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

    def getMap(self, resize = True) -> np.ndarray:
        tmpMap = self.cropArray(Constants.CropOptions.MAP)
        return Screenshot.resize(tmpMap, Constants.Sizes.DESIRED_SIZE) if resize else tmpMap

    @staticmethod
    def resize(arr, size: Constants.Sizes) -> np.ndarray:
        return cv2.resize(arr, size)
    
    def getMapNameFromText(self) -> Optional[str]:
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

        croppedImage = Screenshot.brightenImage(croppedImage, 1, 3, 2)
        
        text = pt.image_to_string(croppedImage)
        
        lines = text.splitlines()
        
        for line in lines:
            text = getMostSimilarText(line.strip())
            
            if text:
                return text
            
        return None
    
    @staticmethod
    def brightenImage(arr : Constants.COLORED_IMAGE, hMult = 1, sMult = 3, vMult = 2):
        hsv = cv2.cvtColor(arr, cv2.COLOR_BGR2HSV)
        
        h, s, v = cv2.split(hsv) # Up sat and brightness
        
        h = cv2.multiply(h, hMult)
        h = np.mod(h, 180)
        
        s = cv2.multiply(s, sMult)
        s = np.clip(s, 0, 255)
        
        v = cv2.multiply(v, vMult)
        v = np.clip(v, 0, 255)
        
        hsv = cv2.merge([h, s, v])
        
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return image

    @staticmethod
    def compareImages(arr1: Constants.COLORED_IMAGE, arr2: Constants.COLORED_IMAGE) -> float:
        grayA = cv2.cvtColor(arr1, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(arr2, cv2.COLOR_BGR2GRAY)
        
        score = ssim(grayA, grayB)
        
        return score
    
    @staticmethod
    def saveImage(arr: Constants.COLORED_IMAGE, fp: str) -> bool:
        try:
            cv2.imwrite(fp, arr)
        except Exception as e:
            return False
        
        return True
    
    def areMapsTheSame(self, screenshot: "Screenshot", thres: float = 0.6) -> bool:
        map1 = self.getMap()
        map2 = screenshot.getMap()
        return self.compareImages(map1, map2) > thres
    
    def checkBountySymbol(self, symbol: Constants.BountyPhases = Constants.BountyPhases.ONE_CLUE) -> bool:
        crop = Constants.CropOptions.BOUNTY_1_PHASE if symbol == Constants.BountyPhases.ONE_CLUE else Constants.CropOptions.BOUNTY_2_PHASE
        croppedImage = self.cropArray(crop)
    
        grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
        
        return np.average(grayImage) > Constants.BOUNTY_SYMBOL_THRES 
    
    def getBountyTotal(self):
        total = 0

        if self.checkBountySymbol(Constants.BountyPhases.ONE_CLUE):
            total += 1

        if self.checkBountySymbol(Constants.BountyPhases.TWO_CLUE):
            total += 1

        return Constants.BountyCount(total)

    
    def getBountyZone(self):
        hsv = cv2.cvtColor(self.getMap(), cv2.COLOR_BGR2HSV)
    
        h, s, v = cv2.split(hsv) # Up sat and brightness
        
        s = cv2.multiply(s, 3)
        s = np.clip(s, 0, 255)
        
        v = cv2.multiply(v, 2)
        v = np.clip(v, 0, 255)
        
        hsv = cv2.merge([h, s, v])
        
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        lowerRange = np.array([0, 0, 100])
        upperRange = np.array([50, 50, 255])
        
        mask = cv2.inRange(image, lowerRange, upperRange)
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        largest_contour = [cnt for cnt in contours if cv2.contourArea(cnt) > 15]
        
        emptyMask = np.zeros_like(image)
        
        cv2.drawContours(emptyMask, largest_contour, -1, (0, 255, 0), thickness=10)
        
        return emptyMask
    
    def fillInside(self):
        # Convert to grayscale
        gray = cv2.cvtColor(self.getMap(), cv2.COLOR_BGR2GRAY)
        
        # Threshold the image to get a binary image
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Assuming the largest contour is the one we want to fill
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Create an empty mask to draw the filled contour
        filled_mask = np.zeros_like(gray)
        
        # Draw the filled contour on the mask
        cv2.drawContours(filled_mask, [largest_contour], -1, color=255, thickness=cv2.FILLED)
        
        return filled_mask
    
    def getCompoundMask(self):
        arr = getBountyZone(self.getMap())
        return fillInside(arr)
    
    def getPhaseNumber(self, bountyNumber: int = 1) -> int:
        """Returns the phase of the bounty based on the number of clues collected for the bounty."""
    
        croppedImage = self.cropArray(CropOptions.BOUNTY_1_NUMBERS if bountyNumber == 1 else CropOptions.BOUNTY_2_NUMBERS)
        
        self.saveImage(croppedImage, str(bountyNumber) + "test.png")
        
        grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
        
        nums = getText(grayImage)
        
        try:
        
            return int(re.search(r"([0-3]+)", nums).group(1))
        
        except AttributeError:
            
            return -1

    def getMapNameFromImage(self, thres: float = 0.6) -> Optional[Constants.Maps]:
        best = -1
        bestName = None
        for name, ss in MAPS.items():
            try:
                result = compareImages(self.getMap(), ss.getMap())
                if result > best:
                    best = result
                    bestName = name
            except:
                pass
            
        if bestName and best > thres:
            match bestName:
                case Constants.Lawson.NAME:
                    return Constants.Lawson
                case Constants.Desalle.NAME:
                    return Constants.Desalle
                case Constants.Stillwater.NAME:
                    return Constants.Stillwater
                
        return None
    
MAPS = {map.NAME : Screenshot(map.PATH) for map in [Constants.Lawson, Constants.Desalle, Constants.Stillwater]}
            