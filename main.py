from flask import Flask, request
from typing import Union, List
from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
import numpy as np
import cv2
from image_processing import *
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session
import scheme
from pydantic import BaseModel
import sqlalchemy.exc as SQLErrors
from sqlalchemy.sql import exists
import constants





APIKey = r"o8QZ3nV6AL%66L6ybai9#z$2YixUw@BD"
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header != APIKey:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key_header

username = APIKeyHeader(name="Username", auto_error=False)

async def get_user(username: str = Depends(username)):
    
    print("Username: " + username)
    
    with constants.session as sesh:
        try:
            sesh.query(exists().where(scheme.User.name == username)).one()
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username",
            )
            
    return username

engine = create_engine('postgresql://happy:password@localhost:5432/hunt', echo = True)

loginRouter = APIRouter(prefix="/api", dependencies=[Depends(get_api_key)]) # "Protected" routes
protectedRouter = APIRouter(prefix="/api", dependencies=[Depends(get_api_key), Depends(get_user)]) # "Protected" routes
app = FastAPI(debug=True)


"""
To run the server, run the following command in the terminal:

hypercorn main:app"""

@app.get('/APIKey') # No depedencies needed
def getAPIKey():
    return {
        "APIKey": APIKey 
    }
    
@protectedRouter.post('/upload')
async def uploadImage(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        
        # Convert the contents to a numpy array
        nparr = np.fromstring(contents, np.uint8)
        
        # Decode the numpy array into an image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        saveImage(img, "test.jpg")
    
        return {
            'status': 'success',
            'message': 'Image uploaded successfully'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
class UserIn(BaseModel):
    username: str
    
@loginRouter.post('/register')
async def register(user: UserIn):
    try:
        with Session(engine) as session:
            session.execute(insert(scheme.User), {"name": user.username})
            session.commit()
        
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
async def login(user: UserIn):
    try:
        with Session(engine) as session:
            user = session.query(scheme.User).filter_by(name=user.username).first()
            
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
