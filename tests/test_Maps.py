from Map import Map
import Constants

def testMapCreationFromFile():
    map = Map("coppedMaps/desalle_full.jpg")
    
    assert(map.getMap().shape == (1440, 3440, 3)) # That its a full size, colored, ultrawide
    
    
def testMapCreationFromBytes():
    
    with open("coppedMaps/desalle_full.jpg", "rb") as f:
        map = Map(f.read())
    
    assert(map.getMap().shape == (1440, 3440, 3)) # That its a full size, colored, ultrawide
    
def testMapCreationGrayScaleBytes():
    with open("coppedMaps/desalle_full.jpg", "rb") as f:
        map = Map(f.read(), True)
    
    assert(map.getMap().shape == (1440, 3440)) # That its a full size, grayscale, ultrawide
    
def testMapCreationGrayScaleFile():
    map = Map("coppedMaps/desalle_full.jpg", True)
    
    assert(map.getMap().shape == (1440, 3440)) # That its a full size, grayscale, ultrawide
    
#_______________________________________________________

def testCropArray():
    map = Map("coppedMaps/desalle_full.jpg")
    
    def cropSize(crop):
        return ( crop[3] - crop[1], crop[2] - crop[0]) # inverted for image testing
    
    croppedMap = map.cropArray(Constants.CropOptions.MAP)
    
    assert(croppedMap.shape == cropSize(Constants.Crops.ULTRA_MAP) + (3,))
    
    map = Map("coppedMaps/desalle_full.jpg")
    
    name = map.cropArray(Constants.CropOptions.NAME)
    
    assert(name.shape == cropSize(Constants.Crops.ULTRA_MAP_NAME) + (3,))
    
    map = Map("tests/testing_images/stillwater_16.9_1B.png")
    
    map = map.cropArray(Constants.CropOptions.MAP)
    
    assert(map.shape == cropSize(Constants.Crops.NORM_MAP) + (3,))
    
    map = Map("tests/testing_images/stillwater_16.9_1B.png")
    
    name = map.cropArray(Constants.CropOptions.NAME)
    
    assert(name.shape == cropSize(Constants.Crops.NORM_MAP_NAME) + (3,))
    
def testIsUltra():
    map = Map("coppedMaps/desalle_full.jpg")
    
    assert(map.isUltra() == True)
    
    map = Map("tests/testing_images/stillwater_16.9_1B.png")
    
    assert(map.isUltra() == False)
    
#_______________________________________________________

def testGetMapNameWithText():
    map = Map("tests/testing_images/stillwater_16.9_1B.png")
    
    assert(map.getMapName() == Constants.Stillwater)
    
    map = Map("tests/testing_images/desalle_full.jpg")
    
    assert(map.getMapName() == Constants.Desalle)
    
    map = Map("tests/testing_images/desalle_16.9_2B.png")
    
    assert(map.getMapName() == Constants.Desalle)