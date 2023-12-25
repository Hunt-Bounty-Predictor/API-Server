from flask import Flask, request
from typing import Union, List
from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
import numpy as np
import cv2
from image_processing import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


app = FastAPI(debug=True)
router = APIRouter(prefix="/api")

APIKey = r"o8QZ3nV6AL%66L6ybai9#z$2YixUw@BD"

engine = create_engine('postgresql://happy:password@localhost:5432/hunt', echo = True)


"""
To run the server, run the following command in the terminal:

hypercorn main:app"""

@router.get('/')
def home():
    return "Hello, World!"

@router.get('/APIKey')
def getAPIKey():
    return {
        "APIKey": APIKey 
    }
    
@router.post('/upload')
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

app.include_router(router)