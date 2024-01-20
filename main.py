from flask import Flask, request
from typing import Union, List
from fastapi import FastAPI, APIRouter, File, Header, UploadFile, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
import numpy as np
import cv2
import image_processing
from sqlalchemy import create_engine, insert, update
from sqlalchemy.orm import Session, joinedload
import scheme
from pydantic import BaseModel
import sqlalchemy.exc as SQLErrors
from sqlalchemy.sql import exists
import Constants
from Constants import session, get_db, get_path
import os
from Screenshot import Screenshot





APIKey = r"o8QZ3nV6AL%66L6ybai9#z$2YixUw@BD"
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header != APIKey:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid API Key",
                "status": "failure"
            },
        )
    return api_key_header

username = APIKeyHeader(name="Username", auto_error=False)

async def get_user(username: str = Depends(username)):
    with session as sesh:
        try:
            sesh.query(exists().where(scheme.User.name == username)).one()
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "User does not exist",
                    "status": "failure"
                },
            )
            
    return username

loginRouter = APIRouter(prefix="/api", dependencies=[Depends(get_api_key)]) # "Protected" routes
protectedRouter = APIRouter(prefix="/api", dependencies=[Depends(get_api_key), Depends(get_user)]) # "Protected" routes
app = FastAPI(debug=True)


"""
To run the server, run the following command in the terminal:

hypercorn main:app"""

@app.get('/api/APIKey') # No depedencies needed
def getAPIKey():
    return {
        "APIKey": APIKey 
    }
    
@protectedRouter.post('/upload')
async def uploadImage(file: UploadFile = File(...), 
                      username : str = Header(None), 
                      db: Session = Depends(get_db),
                      BASE_PATH : str = Depends(get_path)): 

    try:
        with db:
            
            existingUser = db.query(scheme.User).filter_by(name=username).first() # The user is guarenteed to exits, because of the get_user dependency
            contents = await file.read()
            
            ss = Screenshot(contents)
            
            map = ss.getMapName()
            
            if not map:
                raise Exception("not a valid map")
            
            # Process the image
            bountyCount = ss.getCompoundCountInBounty(map.getTownTuples())
            
            if bountyCount == 16:
                # The image is the first image of the map
                # Need to create a primary phase
                
                newImage = scheme.Image(name=file.filename, path=BASE_PATH, is_primary=True, user = existingUser)
                
                newPhase = scheme.PrimaryPhase(image=newImage, map_id = map.ID, user = existingUser)
                
            else:
                # The image is not the first image of the map
                # Need to create a phase
                
                newImage = scheme.Image(name=file.filename, path=BASE_PATH, is_primary=False, user = existingUser)
                
                lastPrimaryPhase = db.query(scheme.PrimaryPhase)\
                    .join(scheme.PrimaryPhase.image)\
                    .filter(scheme.Image.user_id == existingUser.id)\
                    .order_by(scheme.PrimaryPhase.id.desc())\
                    .first()
                
                newPhase = scheme.Phase(image=newImage, primary_phase = lastPrimaryPhase, name = "Empty", phase_number = -1)
                
            db.add(newImage)
            db.add(newPhase)
            db.commit()
            
            db.refresh(newImage)
            
            filePath = os.path.join(BASE_PATH, str(newImage.id) + ".jpg") # Update path

            db.execute(
                update(scheme.Image)
                .where(scheme.Image.id == newImage.id)
                .values(path=filePath))
            db.commit()         
            
            with open(filePath, "wb") as buffer:
                buffer.write(contents)
    
        return {
            'status': 'success',
            'message': 'Image uploaded successfully',
            "phase":newPhase
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={
                "status": "failure",
                "message": str(e)
        })
    
    
class UserIn(BaseModel):
    username: str
    
@loginRouter.post('/register')
async def register(user: UserIn, db: Session = Depends(get_db)):
    try:
        with db:
            db.execute(insert(scheme.User), {"name": user.username})
            db.commit()
        
        return {
            'status': 'success',
            'message': 'User registered successfully'
        }
        
    except SQLErrors.IntegrityError as e:
        raise HTTPException(status_code=409, detail = {"message" : "Username already taken",
                                                       "status" : "failure"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={
                "status": "failure",
                "message": str(e)
                })
    
@loginRouter.post('/login')
async def login(user: UserIn, db: Session = Depends(get_db)):
    try:
        with db:
            user = db.query(scheme.User).filter_by(name=user.username).first()
            
            if user == None:
                raise Exception("User not found")
            
            return {
                'status': 'success',
                'message': 'User logged in successfully'
            }
            
    except SQLErrors.IntegrityError as e:
        raise HTTPException(status_code=409, detail = {"message" : "Username already taken",
                                                       "status" : "failure"})
        

    except Exception as e:
        raise HTTPException(status_code=500, detail={
                "status": "failure",
                "message": str(e)
                })
    

for router in [loginRouter, protectedRouter]:
    app.include_router(router)

#Helo
