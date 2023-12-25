import cv2
from PIL import Image
import pytesseract as pt
from fractions import Fraction
from difflib import SequenceMatcher
from skimage.metrics import structural_similarity as ssim
from errors import *
import numpy as np

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
NORM_MAP = (608, 199, 608 +  701, 199 + 701)
ULTRA_MAP = (1251, 264, 1251 + 937, 264 + 937)

DESIRED_SIZE = (700, 700)

GOLDEN = (367, 0)
SALTERS = (543, 20)
BLANC = (224, 21)
GODARD = (49, 101)
LAWSON = (265, 181)
ARDEN = (436, 227)
WINDY = (595, 270)
SWEETBELL = (327, 339)
MAW = (143, 298)
NICHOLS = (434, 395)
FORT = (238, 416)
IRON = (49, 436)
WOLFS = (48, 585)
LUMBER = (408, 585)
HEMLOCK = (584, 585)
BRADLEY = (265, 603)

LAWSON_POINTS = {
    'GOLDEN': GOLDEN,
    'SALTERS': SALTERS,
    'BLANC': BLANC,
    'GODARD': GODARD,
    'LAWSON': LAWSON,
    'WINDY': WINDY,
    'ARDEN': ARDEN,
    'SWEETBELL': SWEETBELL,
    'MAW': MAW,
    'NICHOLS': NICHOLS,
    'IRON': IRON,
    'FORT': FORT,
    'WOLFS': WOLFS,
    'LUMBER': LUMBER,
    'HEMLOCK': HEMLOCK,
    'BRADLEY': BRADLEY
}

def cropArray(arr, crop):
    return arr[crop[1]:crop[3], crop[0]:crop[2]]

def matchText(text):
    text = text.lower()
    names = {
        "stillwater bayou",
        "lawson delta", 
        "desalle",
    }
    
    for name in names:
        if SequenceMatcher(None, text, name).ratio() > 0.8:
            return name
        
    return "Unknown"

def showImage(arr):
    cv2.imshow('image', arr)
    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)
    
    # closing all open windows
    cv2.destroyAllWindows()

def getText(file):
    f = cv2.imread(file)
    
    height, width = f.shape[:2]

    aspectRatio = Fraction(width, height)
    
    edges = cv2.Canny(f, 400, 200)
    
    if aspectRatio == Fraction(21, 9) or \
        aspectRatio == Fraction(43, 18) or \
        aspectRatio == Fraction(64, 27):
            
        cropped = cropArray(edges, ULTRA_MAP_NAME)
        
    elif aspectRatio == Fraction(16, 9):
        cropped = cropArray(edges, NORM_MAP_NAME)
        
    text = pt.image_to_string(cropped)
    
    lines = text.splitlines()
    
    text = matchText(lines[-1].strip())
        
    return text

def compareImages(image1, image2):

    grayA = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    score = ssim(grayA, grayB)
    
    return score

def isUltra(arr):
    height, width = arr.shape[:2]

    aspectRatio = Fraction(width, height)
    
    if aspectRatio == Fraction(21, 9) or \
        aspectRatio == Fraction(43, 18) or \
        aspectRatio == Fraction(64, 27):
            
        return True
        
    elif aspectRatio == Fraction(16, 9):
        return False
    
    else:
        raise InvalidAspectRatio()

def cropForItem(arr, option : str):
    isArrUltra = isUltra(arr)

    if option == "map":
        return cropArray(arr, ULTRA_MAP if isArrUltra else NORM_MAP)
    
    elif option == "name":
        return cropArray(arr, ULTRA_MAP_NAME if isArrUltra else NORM_MAP_NAME)

def loadImage(file, grayscale = False):
    return cv2.imread(file) if not grayscale else cv2.imread(file, cv2.IMREAD_GRAYSCALE)

def getMap(file, resize = True):
    arr = loadImage(file, True)
    
    arr = cropForItem(arr, "map")
    
    if resize: arr = cv2.resize(arr, DESIRED_SIZE)
    
    return arr

def getEdges(arr):
    return cv2.Canny(arr, 400, 200)

def getCompoundLocations(mapArr):

    # Convert image to grayscale

    #gray_image = cv2.cvtColor(mapArr, cv2.COLOR_BGR2GRAY)
    
    mapArr = getEdges(mapArr)



    # Use Tesseract to detect text and their bounding boxes

    custom_config = r'--oem 3 --psm 11'

    d = pt.image_to_data(mapArr, config=custom_config, output_type=pt.Output.DICT)
    
    print(d)



    # Find the center coordinates of each detected text block

    compound_centers = []

    for i in range(len(d['level'])):

        if int(d['conf'][i]) > 0:  # Confidence level > 0 to ensure some accuracy

            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])

            center_x = x + w / 2

            center_y = y + h / 2

            compound_centers.append((center_x, center_y))
    
    #print(compound_centers)
    
def applyLevels(input_img):

    # Create a lookup table for all possible pixel values

    lut = np.arange(256, dtype='float32')



    # Apply black level (input shadows)

    lut = np.maximum(lut - DARK_POINT, 0) * (255 / (255 - DARK_POINT))



    # Apply white level (input highlights)

    lut = np.minimum(lut, HIGH_POINT) * (255 / HIGH_POINT)



    # Apply gamma correction

    lut = ((lut / 255) ** GAMMA) * 255



    # Ensure values are within [0, 255]

    lut = np.uint8(np.clip(lut, 0, 255))



    # Apply the LUT and return the result

    return cv2.LUT(input_img, lut)

def saveImage(arr, file):
    cv2.imwrite(file, arr)
    
def getCompoundAverage(mapArr, compound, boxSize = 80):
    compound = (compound[0], compound[1], compound[0] + boxSize, compound[1] + boxSize)
    compound = cropArray(mapArr, compound)
    
    return np.average(compound)
    
def getCompoundAverages(mapArr, compounds):
    averages = {}
    
    for compound in compounds:
        averages[compound] = getCompoundAverage(mapArr, compounds[compound])
        
    return averages

def getInBounty(mapArr, compounds, threshold):
    averages = getCompoundAverages(mapArr, compounds)
    
    averages = {}
    
    for compound in compounds:
        avg = getCompoundAverage(mapArr, compounds[compound])
        if avg > threshold:
            averages[compound] = True
        
    return averages

"""Possibly switch to smaller squares to avoid when boss is being banished"""

if __name__ == "__main__":
    image = applyLevels(getMap(r"E:\replays\Hunt Showdown\Map\testing\images\Lawson 2C.jpg", True))
    
    print(getInBounty(image, LAWSON_POINTS, 20))