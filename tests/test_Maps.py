import pytest
from Screenshot import Screenshot
import Constants
import fractions
from tests.TestMap import TestMap, desalle_16_9_2B, desalle_21_9_2B, stillwater_16_9_1B, stillwater_21_9_2B, lawson_21_9_1B, lawson_21_9_2B, testing_maps

ids = [map.NAME for map in testing_maps]

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

@pytest.mark.parametrize("test_map", testing_maps, ids=ids)
def testIsUltra(test_map : TestMap):
    assert test_map.isUltra()
    
def testIsUltra():
    map = Screenshot(desalle_21_9_2B.FILEPATH)
    
    assert(map.isUltra() == True)
    
    map = Screenshot(stillwater_16_9_1B.FILEPATH)
    
    assert(map.isUltra() == False)
    
#_______________________________________________________

@pytest.mark.parametrize("test_map", testing_maps, ids=ids)
def testGetMapNameFromText(test_map : TestMap):
    assert test_map.getMapNameFromText()

def testGetMapNameWithText():
    for map in [stillwater_16_9_1B, desalle_21_9_2B, desalle_16_9_2B]:
        assert map.testGetMapNameWithText()

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

@pytest.mark.parametrize("test_map", testing_maps, ids=ids)
def test_check_bounty_symbol(test_map : TestMap):
    assert test_map.checkBountySymbol()
    
#________________________________________________________

@pytest.mark.parametrize("test_map", testing_maps, ids=ids)
def test_bounty_count(test_map : TestMap):
    assert test_map.testBountyCount()
#________________________________________________________

@pytest.mark.parametrize("test_map", testing_maps, ids=ids)
def test_get_bounty_phase(test_map : TestMap):
    assert test_map.testPhaseDetection()
    
#________________________________________________________

@pytest.mark.parametrize("test_map", testing_maps, ids=ids)
def test_get_map_name_from_image(test_map : TestMap):
    assert test_map.getMapNameFromImage()
    
#________________________________________________________

@pytest.mark.parametrize("test_map", testing_maps, ids=ids)
def test_get_map_name(test_map : TestMap):
    assert test_map.getMapName()

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

@pytest.mark.parametrize("test_map", testing_maps, ids=ids)
def test_get_compund_count(test_map : TestMap):
    assert test_map.getCompundCount()
    
def testGetCompoundCount():
    ss = Screenshot(desalle_21_9_2B.FILEPATH)
    assert(ss.getCompoundCountInBounty(Constants.Desalle.getTownTuples()) == 16)
    
    ss = Screenshot(stillwater_16_9_1B.FILEPATH)
    assert(ss.getCompoundCountInBounty(Constants.Stillwater.getTownTuples()) == 6)
    
    ss = Screenshot(lawson_21_9_2B.FILEPATH)
    assert(ss.getCompoundCountInBounty(Constants.Lawson.getTownTuples()) == 16)

    ss = Screenshot('tests/sequential_images/desalle_three_clues_21_9_qhd.jpg')
    assert(ss.getCompoundCountInBounty(Constants.Desalle.getTownTuples()) == 1)

    ss = Screenshot("tests/sequential_images/desalle_two_clues_21_9_qhd.jpg")
    assert(ss.getCompoundCountInBounty(Constants.Desalle.getTownTuples()) == 6)