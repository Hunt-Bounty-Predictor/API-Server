from image_processing import *
from typing import List, Optional, Union, Literal
import numpy as np
import cv2
import Constants

class Screenshot():
    def __init__(self, screenshot: Union[str, bytes], grayscale = False):
        if isinstance(screenshot, str):
            self.screenshot = self._loadImage(screenshot, grayscale)
        elif isinstance(screenshot, bytes):
            tmp = np.frombuffer(screenshot, np.uint8)
            self.screenshot = cv2.imdecode(tmp, cv2.IMREAD_COLOR)
            if grayscale:
                self.screenshot = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
                
        self.screenshot = self.scaleMap()
    
    def getScreenshot(self) -> Constants.COLORED_IMAGE:
        return self.screenshot
                
    def scaleMap(self):        
        ar = self.getAspectRatio()
        
        if ar == Fraction(16,9):
            return cv2.resize(self.screenshot, (1920, 1080))
        
        return self.screenshot

    def saveMap(self, fp: str) -> bool:
        try:
            saveImage(self.screenshot, fp)
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
                
        return self.getScreenshot()[crop[1]:crop[3], crop[0]:crop[2]]

    def isUltra(self) -> bool:
        aspectRatio = self.getAspectRatio()
        
        if aspectRatio == Fraction(21, 9) or \
            aspectRatio == Fraction(43, 18) or \
            aspectRatio == Fraction(64, 27):
                
            return True
            
        elif aspectRatio == Fraction(16, 9):
            return False
        
    def getAspectRatio(self) -> Fraction:
        height, width = self.getScreenshot().shape[:2]

        return Fraction(width, height)
    
    def getScreenshot(self) -> np.ndarray:
        return self.screenshot

    def getMap(self) -> np.ndarray:
        return self.cropArray(Constants.CropOptions.MAP)
    
    def getMapName(self) -> Optional[str]:
        def getMostSimilarText(text):
            text = text.lower()
            maps : List[Screenshot] = [
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

    @staticmethod
    def compareImages(arr1: Constants.COLORED_IMAGE, arr2: Constants.COLORED_IMAGE) -> float:
        grayA = cv2.cvtColor(arr1, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(arr2, cv2.COLOR_BGR2GRAY)
        
        score = ssim(grayA, grayB)
        
        return score
    
    def areMapsTheSame(self, screenshot: "Screenshot") -> bool:
        map1 = self.getMap()
        map2 = screenshot.getMap()
        return self.compareImages(map1, map2) > 0.8