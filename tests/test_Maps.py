from Screenshot import Screenshot
import Constants
import fractions
from tests.MapInfo import desalle_16_9_2B, desalle_21_9_2B, stillwater_16_9_1B, stillwater_21_9_2B, lawson_21_9_1B, lawson_21_9_2B



def testMapCreationFromFile():
    map = Screenshot(desalle_21_9_2B.FILEPATH)
    
    assert(map.getScreenshot().shape == (1440, 3440, 3)) # That its a full size, colored, ultrawide
    
    
def testMapCreationFromBytes():
    
    with open(desalle_21_9_2B.FILEPATH, "rb") as f:
        map = Screenshot(f.read())
    
    assert(map.getScreenshot().shape == (1440, 3440, 3)) # That its a full size, colored, ultrawide
    
def testMapCreationGrayScaleBytes():
    with open(desalle_21_9_2B.FILEPATH, "rb") as f:
        map = Screenshot(f.read(), True)
    
    assert(map.getScreenshot().shape == (1440, 3440)) # That its a full size, grayscale, ultrawide
    
def testMapCreationGrayScaleFile():
    map = Screenshot(desalle_21_9_2B.FILEPATH, True)
    
    assert(map.getScreenshot().shape == (1440, 3440)) # That its a full size, grayscale, ultrawide
    
#_______________________________________________________

def testCropArray():
    map = Screenshot(desalle_21_9_2B.FILEPATH)
    
    def cropSize(crop):
        return ( crop[3] - crop[1], crop[2] - crop[0]) # inverted for image testing
    
    croppedMap = map.cropArray(Constants.CropOptions.MAP)
    
    assert(croppedMap.shape == cropSize(Constants.Crops.ULTRA_MAP) + (3,))
    
    map = Screenshot(desalle_21_9_2B.FILEPATH)
    
    name = map.cropArray(Constants.CropOptions.NAME)
    
    assert(name.shape == cropSize(Constants.Crops.ULTRA_MAP_NAME) + (3,))
    
    map = Screenshot(stillwater_16_9_1B.FILEPATH)
    
    mapCrop = map.cropArray(Constants.CropOptions.MAP)
    
    assert(mapCrop.shape == cropSize(Constants.Crops.NORM_MAP) + (3,))
    
    map = Screenshot(stillwater_16_9_1B.FILEPATH)
    
    name = map.cropArray(Constants.CropOptions.NAME)
    
    assert(name.shape == cropSize(Constants.Crops.NORM_MAP_NAME) + (3,))

#_______________________________________________________
    
def testIsUltra():
    map = Screenshot(desalle_21_9_2B.FILEPATH)
    
    assert(map.isUltra() == True)
    
    map = Screenshot(stillwater_16_9_1B.FILEPATH)
    
    assert(map.isUltra() == False)
    
#_______________________________________________________

def testGetMapNameWithText():
    map = Screenshot(stillwater_16_9_1B.FILEPATH)
    
    assert(map.getMapNameFromText() == Constants.Stillwater)
    
    map = Screenshot(desalle_21_9_2B.FILEPATH)
    
    assert(map.getMapNameFromText() == Constants.Desalle)
    
    map = Screenshot(desalle_16_9_2B.FILEPATH)
    
    assert(map.getMapNameFromText() == Constants.Desalle)

#________________________________________________________

def testGetMapResize():
    map = Screenshot(desalle_21_9_2B.FILEPATH)

    assert(map.getMap().shape == Constants.Sizes.DESIRED_SIZE + (3,))

def testGetMapNoResize():
    map = Screenshot(desalle_21_9_2B.FILEPATH)

    shape = map.getMap(False).shape

    assert(shape[0] == shape[1])

#________________________________________________________
    
def testCompareImages():
    map1 = Screenshot(stillwater_16_9_1B.FILEPATH)
    map2 = Screenshot(stillwater_21_9_2B.FILEPATH)

    assert(map1.areMapsTheSame(map2) == True)

    map1 = Screenshot(desalle_16_9_2B.FILEPATH)
    map2 = Screenshot(desalle_21_9_2B.FILEPATH)

    assert(map1.areMapsTheSame(map2) == True)

    map1 = Screenshot(desalle_16_9_2B.FILEPATH)
    map2 = Screenshot(stillwater_21_9_2B.FILEPATH)

    assert(map1.areMapsTheSame(map2) == False)

#________________________________________________________

def testGetBountyPhase():
    ss = Screenshot(desalle_21_9_2B.FILEPATH)

    assert(ss.checkBountySymbol() == True)

    assert(ss.checkBountySymbol(Constants.BountyPhases.TWO_CLUE) == True)

    ss = Screenshot(stillwater_16_9_1B.FILEPATH)

    assert (ss.checkBountySymbol() == True)

    assert (ss.checkBountySymbol(Constants.BountyPhases.TWO_CLUE) == False)

def testBountyCount():
    ss = Screenshot(desalle_21_9_2B.FILEPATH)

    assert(ss.getBountyTotal() == Constants.BountyCount.TWO)

    ss = Screenshot(stillwater_16_9_1B.FILEPATH)

    assert(ss.getBountyTotal() == Constants.BountyCount.ONE)

    ss = Screenshot(desalle_16_9_2B.FILEPATH)

    assert(ss.getBountyTotal() == Constants.BountyCount.TWO)
    
#________________________________________________________

def testPhaseDetection():
    ss = Screenshot(lawson_21_9_1B.FILEPATH)
    
    assert(ss.getPhaseNumber(1) == 0)
    
    assert(ss.getPhaseNumber(2) == -1)
    
    ss = Screenshot(lawson_21_9_2B.FILEPATH)
    
    assert(ss.getPhaseNumber(1) == 0)
    
    assert(ss.getPhaseNumber(2) == 0)
    
    ss = Screenshot(desalle_16_9_2B.FILEPATH)
    
    assert(ss.getPhaseNumber(1) == -1)
    
    assert(ss.getPhaseNumber(2) == -1)
    
    ss = Screenshot(stillwater_16_9_1B.FILEPATH)
    
    assert(ss.getPhaseNumber(1) == 2)
    
    assert(ss.getPhaseNumber(2) == -1)
    
#________________________________________________________

def testGetMapFromImage():
    
    ss = Screenshot(desalle_21_9_2B.FILEPATH)
    assert(ss.getMapNameFromImage() == Constants.Desalle)
    
    ss = Screenshot(stillwater_16_9_1B.FILEPATH)
    assert(ss.getMapNameFromImage() == Constants.Stillwater)
    
    ss = Screenshot("tests/map_comparision_tests/desalle_21.9_2B.jpg")
    assert(ss.getMapNameFromImage() == Constants.Desalle)
    
    ss = Screenshot("tests/map_comparision_tests/lawson_21.9_1B.jpg")
    assert(ss.getMapNameFromImage() == Constants.Lawson)
    
    ss = Screenshot("tests/map_comparision_tests/lawson_21.9_2B.jpg")
    assert(ss.getMapNameFromImage() == Constants.Lawson)
    
    ss = Screenshot("tests/map_comparision_tests/stillwater_21.9_2B.jpg")
    assert(ss.getMapNameFromImage() == Constants.Stillwater)

def testGetMapName():
    ss = Screenshot(desalle_21_9_2B.FILEPATH)
    assert(ss.getMapName() == Constants.Desalle)
    
    ss = Screenshot(stillwater_16_9_1B.FILEPATH)
    assert(ss.getMapName() == Constants.Stillwater)
    
    ss = Screenshot("tests/map_comparision_tests/desalle_21.9_2B.jpg")
    assert(ss.getMapName() == Constants.Desalle)
    
    ss = Screenshot("tests/map_comparision_tests/lawson_21.9_1B.jpg")
    assert(ss.getMapName() == Constants.Lawson)
    
    ss = Screenshot("tests/map_comparision_tests/lawson_21.9_2B.jpg")
    assert(ss.getMapName() == Constants.Lawson)
    
    ss = Screenshot("tests/map_comparision_tests/stillwater_21.9_2B.jpg")
    assert(ss.getMapName() == Constants.Stillwater)
    
    ss = Screenshot("tests/map_comparision_tests/stillwater_21.9_2B.jpg")
    assert(ss.getMapName() == Constants.Stillwater)
    
    ss = Screenshot("tests/map_comparision_tests/desalle_21.9_2B.jpg")
    assert(ss.getMapName() == Constants.Desalle)
    
#________________________________________________________
    
def testGetCompoundCount():
    ss = Screenshot(desalle_21_9_2B.FILEPATH)
    assert(ss.getCompoundCountInBounty(Constants.Desalle.getTownTuples()) == 16)
    
    ss = Screenshot(stillwater_16_9_1B.FILEPATH)
    assert(ss.getCompoundCountInBounty(Constants.Stillwater.getTownTuples()) == 6)
    
    ss = Screenshot(lawson_21_9_2B.FILEPATH)
    assert(ss.getCompoundCountInBounty(Constants.Lawson.getTownTuples()) == 16)