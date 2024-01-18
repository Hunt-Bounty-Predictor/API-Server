from Map import Map
import Constants
import fractions
from tests.MapInfo import desalle_16_9_2B, desalle_21_9_2B, stillwater_16_9_1B, stillwater_21_9_2B



def testMapCreationFromFile():
    map = Map(desalle_21_9_2B.FILEPATH)
    
    assert(map.getMap().shape == (1440, 3440, 3)) # That its a full size, colored, ultrawide
    
    
def testMapCreationFromBytes():
    
    with open(desalle_21_9_2B.FILEPATH, "rb") as f:
        map = Map(f.read())
    
    assert(map.getMap().shape == (1440, 3440, 3)) # That its a full size, colored, ultrawide
    
def testMapCreationGrayScaleBytes():
    with open(desalle_21_9_2B.FILEPATH, "rb") as f:
        map = Map(f.read(), True)
    
    assert(map.getMap().shape == (1440, 3440)) # That its a full size, grayscale, ultrawide
    
def testMapCreationGrayScaleFile():
    map = Map(desalle_21_9_2B.FILEPATH, True)
    
    assert(map.getMap().shape == (1440, 3440)) # That its a full size, grayscale, ultrawide
    
#_______________________________________________________

def testCropArray():
    map = Map(desalle_21_9_2B.FILEPATH)
    
    def cropSize(crop):
        return ( crop[3] - crop[1], crop[2] - crop[0]) # inverted for image testing
    
    croppedMap = map.cropArray(Constants.CropOptions.MAP)
    
    assert(croppedMap.shape == cropSize(Constants.Crops.ULTRA_MAP) + (3,))
    
    map = Map(desalle_21_9_2B.FILEPATH)
    
    name = map.cropArray(Constants.CropOptions.NAME)
    
    assert(name.shape == cropSize(Constants.Crops.ULTRA_MAP_NAME) + (3,))
    
    map = Map(stillwater_16_9_1B.FILEPATH)
    
    map = map.cropArray(Constants.CropOptions.MAP)
    
    assert(map.shape == cropSize(Constants.Crops.NORM_MAP) + (3,))
    
    map = Map(stillwater_16_9_1B.FILEPATH)
    
    name = map.cropArray(Constants.CropOptions.NAME)
    
    assert(name.shape == cropSize(Constants.Crops.NORM_MAP_NAME) + (3,))
    
def testIsUltra():
    map = Map(desalle_21_9_2B.FILEPATH)
    
    assert(map.isUltra() == True)
    
    map = Map(stillwater_16_9_1B.FILEPATH)
    
    assert(map.isUltra() == False)
    
#_______________________________________________________

def testGetMapNameWithText():
    map = Map(stillwater_16_9_1B.FILEPATH)
    
    assert(map.getMapName() == Constants.Stillwater)
    
    map = Map(desalle_21_9_2B.FILEPATH)
    
    assert(map.getMapName() == Constants.Desalle)
    
    map = Map(desalle_16_9_2B.FILEPATH)
    
    assert(map.getMapName() == Constants.Desalle)