from image_processing import *
from typing import List, Optional, Union, Literal
import numpy as np
import cv2
import Constants

class Map():
    def __init__(self, map: Union[str, bytes], grayscale = False):
        if isinstance(map, str):
            self.map = self._loadImage(map, grayscale)
        elif isinstance(map, bytes):
            tmp = np.frombuffer(map, np.uint8)
            self.map = cv2.imdecode(tmp, cv2.IMREAD_COLOR)
            if grayscale:
                self.map = cv2.cvtColor(self.map, cv2.COLOR_BGR2GRAY)
                
        self.map = self.scaleMap()
                
    def scaleMap(self):
        
        ar = self.getAspectRatio()
        
        if ar == Fraction(16,9):
            return cv2.resize(self.map, (1920, 1080))
        
        return self.map

    def saveMap(self, fp: str) -> bool:
        try:
            saveImage(self.map, fp)
        except Exception as e:
            return False
        
        return True
    
    def _loadImage(self, fp: str, grayscale = False) -> np.ndarray:
        image = cv2.imread(fp, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
        return image
    
    def cropArray(self, target: Constants.CropOptions):
        isUltra = self.isUltra()
        
        match target:
            case Constants.CropOptions.MAP:
                crop = Constants.Crops.ULTRA_MAP if isUltra else Constants.Crops.NORM_MAP
                
            case Constants.CropOptions.NAME:
                crop = Constants.Crops.ULTRA_MAP_NAME if isUltra else Constants.Crops.NORM_MAP_NAME
                
            case Constants.CropOptions.BOUNTY_1_NUMBERS:
                crop = Constants.Crops.ULTRA_BOUNTY_1_NUMS if isUltra else Constants.Crops.NORMAL_BOUNTY_1_NUMS
                
            case Constants.CropOptions.BOUNTY_1_PHASE:
                crop = Constants.Crops.ULTRA_BOUNTY_1_PHASE if isUltra else Constants.Crops.NORMAL_BOUNTY_1_PHASE
                
            case Constants.CropOptions.BOUNTY_2_NUMBERS:
                crop = Constants.Crops.ULTRA_BOUNTY_2_NUMS if isUltra else Constants.Crops.NORMAL_BOUNTY_2_NUMS
                
            case Constants.CropOptions.BOUNTY_2_PHASE:
                crop = Constants.Crops.ULTRA_BOUNTY_2_PHASE if isUltra else Constants.Crops.NORMAL_BOUNTY_2_PHASE
                
        return self.getMap()[crop[1]:crop[3], crop[0]:crop[2]]
        
    def isUltra(self) -> bool:
        aspectRatio = self.getAspectRatio()
        
        if aspectRatio == Fraction(21, 9) or \
            aspectRatio == Fraction(43, 18) or \
            aspectRatio == Fraction(64, 27):
                
            return True
            
        elif aspectRatio == Fraction(16, 9):
            return False
        
    def getAspectRatio(self) -> Fraction:
        height, width = self.getMap().shape[:2]

        return Fraction(width, height)
    
    def getMap(self) -> np.ndarray:
        return self.map
    
    def getMapName(self) -> Optional[str]:
        def getMostSimilarText(text):
            text = text.lower()
            maps : List[Map] = [
                Constants.Stillwater,
                Constants.Lawson,
                Constants.Desalle
            ]
            
            for m in maps:
                if SequenceMatcher(None, text, m.NAME).ratio() > 0.8:
                    return m
                
            return None
        
        croppedImage = self.cropArray(Constants.CropOptions.NAME)
        
        text = pt.image_to_string(croppedImage)
    
        lines = text.splitlines()
        
        for line in lines:
            text = getMostSimilarText(line.strip())
            
            if text:
                return text
            
        return None