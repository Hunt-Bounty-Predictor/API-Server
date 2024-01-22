from image_processing import *
from typing import List, Optional, Tuple, Union, Literal
import numpy as np
import cv2
import Constants

class Screenshot():
    def __init__(self, screenshot: Union[str, bytes], grayscale = False):
        """Create a screenshot based on either a filepath or a bytes object.

        Args:
            screenshot (Union[str, bytes]): The screenshot to load. 
            It can either be a bytes object (From an api upload ;)) 
            or a filepath on the local system.

            grayscale (bool, optional): Defaults to False. Whether or not to load the image in grayscale.

        Raises:
            TypeError: Raised if the passed in screenshot is not a string or bytes.
        """
        if isinstance(screenshot, str):
            self.screenshot = self._loadImage(screenshot, grayscale)
        elif isinstance(screenshot, bytes):
            tmp = np.frombuffer(screenshot, np.uint8)
            self.screenshot = cv2.imdecode(tmp, cv2.IMREAD_COLOR)
            if grayscale:
                self.screenshot = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)
                
        else:
            raise TypeError("Screenshot must be either a string or bytes.")
                
        self.screenshot = self.scaleMap() # We need to ensure a standard size so we do not need
                                          # to maintain multiple crops and bounty locations.
    
    def getScreenshot(self) -> np.ndarray:
        """Returns the screenshot within. Represented as a numpy array.

        Returns:
            Constants.COLORED_IMAGE: Numpy array representing the screenshot, Can be either grayscale or color.
        """
        return self.screenshot
                
    def scaleMap(self) -> np.ndarray:     
        """Scales the map to a standard size. 
        These standard sizes are 1920x1080 for 16:9 and 3440x1440 for 21:9.
        Our goal is to have a standard size so we do not need to maintain multiple crops and bounty locations.

        Returns:
            np.ndarray: The image that is resized.
        """
        ar = self.getAspectRatio()
        
        if ar == Fraction(16,9):
            return cv2.resize(self.screenshot, (1920, 1080))
        
        elif self.isUltra():
            return cv2.resize(self.screenshot, (3440, 1440))
        
        return self.screenshot # Already a valid size

    def saveMap(self, fp: str) -> bool:
        """Save the current screenshot to a file.

        Args:
            fp (str): The filepath the screenshot will be saved to.

        Returns:
            bool: if the saving was successful.
        """
        try:
            cv2.imwrite(self.getScreenshot(), fp)
        except Exception as e:
            return False
        
        return True
    
    def _loadImage(self, fp: str, grayscale = False) -> np.ndarray:
        """Loads an image from a filepath.

        Args:
            fp (str): The filepath of the image to load
            grayscale (bool, optional): Defaults to False. Should the image be loaded in grayscale

        Returns:
            np.ndarray: The image that was loaded.
        """
        image = cv2.imread(fp, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
        return image

    def cropArray(self, target: Constants.CropOptions) -> np.ndarray:
        """Crops the current screenshot based on the target.

        Args:
            target (Constants.CropOptions): The target to crop the screenshot to.
            There are a number of options.
            Please view the CropOptions enum for more information.

        Returns:
            np.ndarray: The resulting cropped image. 
        """
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
        """Determines if the image is an ultrawide image. (21:9 aspect ratio)

        Detects HD, FHD, QHD, and UHD (21:9, 43:18, 64:27) ultrawide images.

        All other ratios are considered non Ultrawide.

        Returns:
            bool: If the image is an ultrawide image.
        """
        aspectRatio = self.getAspectRatio()
        
        if aspectRatio in Constants.ULTRA_WIDE.getRatios():
                
            return True
            
        elif aspectRatio in Constants.NORMAL.getRatios():
            return False
        
    def getAspectRatio(self) -> Fraction:
        """Returns the aspect ratio of the image in the form of a fraction.

        Returns:
            Fraction: The aspect ratio of the image. The numerator is the width and the denominator is the height.
        """
        height, width = self.getScreenshot().shape[:2]

        return Fraction(width, height)
    
    def getScreenshot(self) -> np.ndarray:
        """Returns the screenshot within. Represented as a numpy array.

        Returns:
            np.ndarray: The current image loaded.
        """
        return self.screenshot

    def getMap(self, resize = True) -> np.ndarray:
        """Gets the current map in the screenshot. Determines the crop location for you.

        Args:
            resize (bool, optional): _description_. Defaults to True.
            This is if the cropped map should be resized to the standard Constants.Sizes.DESIRED_SIZE.

        Returns:
            np.ndarray: The map within the screenshot.
        """
        tmpMap = self.cropArray(Constants.CropOptions.MAP)
        return Screenshot.resize(tmpMap, Constants.Sizes.DESIRED_SIZE) if resize else tmpMap

    @staticmethod
    def resize(arr, size: Constants.Sizes) -> np.ndarray:
        """Resizes the given image to the given size.

        Args:
            arr (_type_): The image to resize
            size (Constants.Sizes): The size to resize it to.

        Returns:
            np.ndarray: The resized image.
        """
        return cv2.resize(arr, size)
    
    def getMapNameFromText(self) -> Optional[Constants.Maps]:
        """Gets the name of the map based on the map name at the top of the map.
        Sometimes this text may be obstructed by the bounty UI.
        So you may need to utilize image comparision to get the map name.

        Returns:
            Optional[Constants.Maps]: The map name if it was found. None otherwise.
        """
        def getMostSimilarText(text: str) -> Optional[Constants.Maps]:
            """Tries to find the most similar text to the given text.
            Sometimes the text given may not be the exact text of the map name.

            Args:
                text (str): The text to compare to the map names.

            Returns:
                Optional[Constants.Maps]: The map name if it was found. None otherwise.
            """
            text = text.lower()
            maps : List[Screenshot] = [
                Constants.Stillwater,
                Constants.Lawson,
                Constants.Desalle
            ]
            
            for m in maps:
                if SequenceMatcher(None, text, m.NAME).ratio() > 0.8: # Magic number :) 
                                                                      # Essentially if the text is 80% similar to the map name.
                    return m
                
            return None
        
        croppedImage = self.cropArray(Constants.CropOptions.NAME)

        croppedImage = Screenshot.brightenImage(croppedImage, 1, 3, 2) # Brighten the image to make the text more readable.
        
        text = pt.image_to_string(croppedImage)
        
        lines = text.splitlines()
        
        for line in lines:
            text = getMostSimilarText(line.strip())
            
            if text:
                return text
            
        return None
    
    def getMapNameFromImage(self, thres: float = 0.6) -> Optional[Constants.Maps]:
        """_summary_

        Args:
            thres (float, optional): _description_. Defaults to 0.6.

        Returns:
            Optional[Constants.Maps]: _description_
        """
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
    
    def getMapName(self) -> Optional[Constants.Maps]:
        """Attempts to get the map name.
        This First attempts to get the map name from the text.
        Then it tries image comparision to get the map name.

        Returns:
            Optional[Constants.Maps]: The name of the given map. None if the map name could not be found.
        """
        map = self.getMapNameFromText()
        if not map:
            map = self.getMapNameFromImage()
            
        return map
    
    
    @staticmethod
    def brightenImage(arr : Constants.COLORED_IMAGE, hMult = 1, sMult = 3, vMult = 2) -> Constants.COLORED_IMAGE:
        """Adjust an image in the HSV color space.
        The default values brighten an image.

        Args:
            arr (Constants.COLORED_IMAGE): The image to brighten.
            hMult (int, optional): _description_. Defaults to 1. Hue
            sMult (int, optional): _description_. Defaults to 3. Saturation
            vMult (int, optional): _description_. Defaults to 2. Value

        Returns:
            Constants.COLORED_IMAGE: The brightened image.
        """
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
        """Compares two images using the SSIM algorithm.
        The images must be the same size.


        Args:
            arr1 (Constants.COLORED_IMAGE): The first image to compare.
            arr2 (Constants.COLORED_IMAGE): The second image to compare.

        Returns:
            float: The similarity of the two images. 1.0 is the same image.
        """
        grayA = cv2.cvtColor(arr1, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(arr2, cv2.COLOR_BGR2GRAY)
        
        score = ssim(grayA, grayB)
        
        return score
    
    @staticmethod
    def saveImage(arr: Constants.COLORED_IMAGE, fp: str) -> bool:
        """Saves an image to a file.

        Args:
            arr (Constants.COLORED_IMAGE): The image to save
            fp (str): The filepath to save the image to.

        Returns:
            bool: If the saving was successful.
        """
        try:
            cv2.imwrite(fp, arr)
        except Exception as e:
            return False
        
        return True
    
    def areMapsTheSame(self, screenshot: "Screenshot", thres: float = 0.6) -> bool:
        """Determines if the current screenshot is the same as the given screenshot.

        Right now it it crops the maps out automatically and compares them.

        _This needs to be moved to a static method or a new class based on only maps_

        Args:
            screenshot (Screenshot): The screenshot to compare too.
            thres (float, optional): Defaults to 0.6. What is the threshold for the images to be considered the same.

        Returns:
            bool: If the maps are the same
        """
        map1 = self.getMap()
        map2 = screenshot.getMap()
        return self.compareImages(map1, map2) > thres
    
    def checkBountySymbol(self, bounty: int = 1) -> bool:
        """Check if a bounty exists. This should help you determine how many bountys are on a map.

        Args:
            bounty (int, optional): Defaults to 1. The bounty to check. There are at most 2.

        Returns:
            bool: If that bounty exists.
        """
        crop = Constants.CropOptions.BOUNTY_1_PHASE if bounty == 1 else Constants.CropOptions.BOUNTY_2_PHASE
        croppedImage = self.cropArray(crop)
    
        grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
        
        return np.average(grayImage) > Constants.BOUNTY_SYMBOL_THRES 
        # The bounty symbols are a light grey surrounded by a dark grey. 
    
    def getBountyTotal(self) -> int:
        """Gets the total number of bountys on the map.

        Returns:
            int: The total number of bountys on the map.
        """
        total = 0

        if self.checkBountySymbol(1):
            total += 1

        if self.checkBountySymbol(2):
            total += 1

        return total
    
    def getPhaseNumber(self, bountyNumber: int = 1) -> int:
        """Attempts to get the number of clues gathered for a given bounty.

        Args:
            bountyNumber (int, optional): Defaults to 1. The bounty to check.

        Returns:
            int: The number of clues gathered for the given bounty.
        """
    
        croppedImage = self.cropArray(CropOptions.BOUNTY_1_NUMBERS if bountyNumber == 1 else CropOptions.BOUNTY_2_NUMBERS)
        
        grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
        
        nums = getText(grayImage)
        
        try:
        
            return int(re.search(r"([0-3]+)", nums).group(1))
        
        except AttributeError:
            
            if self.checkBountySymbol(bountyNumber):
                return 3
            
            return -1


    
    def getBountyZone(self) -> np.ndarray:
        """Determines the bounty zone on the map. This is the area the bounty can be found in.

        Returns:
            np.ndarray: The mask of the bounty zone.
        """
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
        
        cv2.drawContours(emptyMask, largest_contour, -1, (0, 255, 0), thickness=13)
        
        return emptyMask
    
    @staticmethod
    def fillInside(arr: np.ndarray) -> np.ndarray:
        """Fills the inside of given image with a large polygon.

        Returns:
            np.ndarray: The filled image.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        
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
    
    def getCompoundMask(self) -> np.ndarray:
        """Gets the mask of a map on in the screenshot.
        Useful for determining if a compound is in the bounty zone.

        Returns:
            np.ndarray: The filled in mask of the map.
        """
        arr = self.getBountyZone()
        return self.fillInside(arr)    
   
    @staticmethod 
    def isPointInMask(mask, point: tuple) -> bool:
        """Detrmines if a point is in a mask.

        Returns:
            bool: If the point is in the mask.
        """
        return mask[point[1], point[0]] == 255


    def getCompoundCountInBounty(self, compounds : Tuple[int, int]) -> int:
        """Counts the number of compounds in the bounty zone.

        Args:
            compounds (Tuple[int, int]): The compunds to count

        Returns:
            int: The number of compounds in the bounty zone.
        """
        maskedImage = self.getCompoundMask()

        return sum([Screenshot.isPointInMask(maskedImage, point) for point in compounds])
    
    def getCompoundStatus(self, compounds: Tuple[int, int]) -> List[bool]:
        """Determines if the compounds are in the bounty zone.

        Args:
            compounds (Tuple[int, int]): The compounds to check.

        Returns:
            List[bool]: The status of the compounds.
        """
        maskedImage = self.getCompoundMask()
        
        return [Screenshot.isPointInMask(maskedImage, point) for point in compounds]

    
MAPS = {map.NAME : Screenshot(map.PATH) for map in [Constants.Lawson, Constants.Desalle, Constants.Stillwater]}
            