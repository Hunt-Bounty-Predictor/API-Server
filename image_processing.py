from PIL import Image
import cv2
from PIL import Image
import pytesseract as pt
from fractions import Fraction
from difflib import SequenceMatcher
from skimage.metrics import structural_similarity as ssim
from errors import *
import numpy as np
import os
from Constants import Crops, CropOptions, BountyPhases, COLORED_IMAGE
import Constants
import re
import numpy

ULTRAx = 1254
ULTRAy = 170
ULTRAwidth = 926
ULTRAheight = 75

NORMx = 608
NORMy = 115
NORMwidth = 699
NORMheight = 71

DARK_POINT = 87

HIGH_POINT = 157

GAMMA = 1.28

ULTRA_MAP_NAME = (ULTRAx, ULTRAy, ULTRAx + ULTRAwidth, ULTRAy + ULTRAheight)
NORM_MAP_NAME = (NORMx, NORMy, NORMx + NORMwidth, NORMy + NORMheight)
NORM_MAP = (600, 190, 600 +  720, 190 + 720)
ULTRA_MAP = (1240, 255, 1240 + 950, 255 + 950)

DESIRED_SIZE = (700, 700)

from Constants import Lawson

#from scripts import populateTownsLawson

def cropArray(arr, crop): #
    return arr[crop[1]:crop[3], crop[0]:crop[2]]

def getMostSimilarText(text):
    text = text.lower()
    names = {
        "stillwater bayou",
        "lawson delta", 
        "desalle",
    }
    
    for name in names:
        if SequenceMatcher(None, text, name).ratio() > 0.8:
            return name
        
    return None

def showImage(arr):
    cv2.imshow('image', arr)
    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)
    
    # closing all open windows
    cv2.destroyAllWindows()
    
def getText(arr) -> str:
    return pt.image_to_string(arr)

def getmapNameBasedOnText(arr):
            
    text = pt.image_to_string(arr)
    
    lines = text.splitlines()
    
    text = getMostSimilarText(lines[-1].strip())
        
    return text

def compareImages(image1, image2):

    grayA = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    score = ssim(grayA, grayB)
    
    return score

def isUltra(arr): #
    height, width = arr.shape[:2]

    aspectRatio = Fraction(width, height)
    
    if aspectRatio == Fraction(21, 9) or \
        aspectRatio == Fraction(43, 18) or \
        aspectRatio == Fraction(64, 27):
            
        return True
        
    elif aspectRatio == Fraction(16, 9):
        return False
    
    else:
        raise InvalidAspectRatio(message = str(arr.shape[:2]))
    
    
def getMapNameBasedOnImage(arr, imagePath):
    for imageName in os.listdir(imagePath):
        image = cv2.imread(imagePath + imageName)
        
        assert image is not None
        if image.shape != arr.shape:
            image = cv2.resize(image, DESIRED_SIZE)
        
        if compareImages(arr, image) > 0.6:
            return imageName.split('.')[0]
        
    return None
        
        
def getMapName(uncroppedImage):
    """
    Accepts the path to an image and returns the name of the map."""
    
    uncroppedImage
    
    text = getmapNameBasedOnText(cropForItem(uncroppedImage, "name"))
    
    if text:
        return text
    
    else:
        uncroppedImage = cropForItem(uncroppedImage, "map")
        uncroppedImage = cv2.resize(uncroppedImage, DESIRED_SIZE)
        return getMapNameBasedOnImage(uncroppedImage, r'/mnt/e/replays/Hunt Showdown/Map/testing/images/defaultMaps/')
    

def cropForItem(arr, option : str):
    
    isArrUltra = isUltra(arr)

    if option == CropOptions.MAP:
        mapArr = cropArray(arr, ULTRA_MAP if isArrUltra else NORM_MAP)
        
        return cv2.resize(mapArr, Constants.Crops.DESIRED_SIZE)
    
    elif option == CropOptions.NAME:
        return cropArray(arr, ULTRA_MAP_NAME if isArrUltra else NORM_MAP_NAME)
    
    elif option == CropOptions.BOUNTY_1_NUMBERS:
        return cropArray(arr, Crops.ULTRA_BOUNTY_1_NUMS if isArrUltra else Crops.NORMAL_BOUNTY_1_NUMS)
    
    elif option == CropOptions.BOUNTY_1_PHASE:
        return cropArray(arr, Crops.ULTRA_BOUNTY_1_PHASE if isArrUltra else Crops.NORMAL_BOUNTY_1_PHASE)
    
    elif option == CropOptions.BOUNTY_2_NUMBERS:
        return cropArray(arr, Crops.ULTRA_BOUNTY_2_NUMS if isArrUltra else Crops.NORMAL_BOUNTY_2_NUMS)
    
    elif option == CropOptions.BOUNTY_2_PHASE:
        return cropArray(arr, Crops.ULTRA_BOUNTY_2_PHASE if isArrUltra else Crops.NORMAL_BOUNTY_2_PHASE)
        

def loadImage(file, grayscale = False):
    return cv2.imread(file) if not grayscale else cv2.imread(file, cv2.IMREAD_GRAYSCALE)

def getMap(file, resize = True, grayscale = False):
    arr = loadImage(file, grayscale)
    
    arr = cropForItem(arr, CropOptions.MAP)
    
    if resize: arr = cv2.resize(arr, Constants.Crops.DESIRED_SIZE)
    
    return arr

def getEdges(arr):
    return cv2.Canny(arr, 400, 200)


def saveImage(arr, file):
    cv2.imwrite(file, arr)


def drawContours(arr, contours):
    # Draw all contours
    # -1 signifies drawing all contours
    cv2.drawContours(arr, contours, -1, (0, 255, 0), thickness=cv2.FILLED)
    
    return arr

def makeContourShape(arr, contours):
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    
    for contour in contours:
        cv2.drawContours(mask, [contour], -1, (255), thickness=7)
        
    unified_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return unified_contours

def isPointInMask(mask, point: tuple):
    return mask[point[1], point[0]] == 255


def getCompoundCountInBounty(mapArr, compounds) -> Constants.BountyPhases:
    maskedImage = getCompoundMask(mapArr)
    
    saveImage(maskedImage, r'/mnt/e/replays/Hunt Showdown/Map/testing/images/Lawson0CMasked.jpg')

    return sum([isPointInMask(maskedImage, point) for point in compounds])
    
def getBountyPhase(image : COLORED_IMAGE, bountyNumber : int = 1) -> BountyPhases:
    
    """Returns the phase of the bounty based on the number of clues collected for the bounty."""
    
    croppedImage = cropForItem(image, CropOptions.BOUNTY_1_NUMBERS if bountyNumber == 1 else CropOptions.BOUNTY_2_NUMBERS)
    
    grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
    
    nums = getText(grayImage)
    
    try:
    
        return BountyPhases(int(re.search(r"([0-3]+)", nums).group(1))) 
    
    except AttributeError:
        
        return -1

def getNumberOfBounties(image : COLORED_IMAGE) -> Constants.BountyCount:
    """Returns the number of bounties on the map."""
    total = 0
    
    if checkBountyPhaseSymbol(image, 1) != -1:
        total += 1
        
    if checkBountyPhaseSymbol(image, 2) != -1:
        total += 1
        
    assert total > 0 and total < 3
    
    return Constants.BountyCount(total)

def brightenImage(arr, hMult, sMult, vMult):
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

def getBountyZone(mapArr : COLORED_IMAGE):
    hsv = cv2.cvtColor(mapArr, cv2.COLOR_BGR2HSV)
    
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
    
def fillInside(arr):
    """Fills the inside of largest contour in the image."""
    
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

def getCompoundMask(arr) -> Constants.GRAYSCALE_IMAGE:
    arr = getBountyZone(arr)
    return fillInside(arr)

def drawPoints(arr, points):
    arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    for point in points:
        cv2.circle(arr, point, 5, (0, 0, 255), -1)
        
    return arr

def checkBountyPhaseSymbol(arr, symbol = 1):
    """Returns true if the bounty phase symbol is present in the image."""
    
    croppedImage = cropForItem(arr, CropOptions.BOUNTY_1_PHASE if symbol == 1 else CropOptions.BOUNTY_2_PHASE)
    
    grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
    
    return np.average(grayImage) > Constants.BOUNTY_SYMBOL_THRES

if __name__ == "__main__":
    image = getMap(r'/home/oliver/images/coppedMaps/stillwater_full.jpg')
    saveImage(image, r'/home/oliver/images/coppedMaps/stillwater_cropped.jpeg')
    
    