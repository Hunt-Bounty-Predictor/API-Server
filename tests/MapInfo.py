from Screenshot import Screenshot
import Constants
import fractions
import re

class TestMap():
    FILEPATH: str
    ASPECT_RATIO: fractions.Fraction
    MAP: Constants.Map
    BOUNTY_COUNT: int

    def __init__(self, filepath: str, 
                 aspect_ratio: fractions.Fraction, 
                 map: Constants.Map, 
                 bounty_count: int, 
                 compounds_in_zone: int = 0,
                 bounty1_phase_number: int = 0,
                 bounty2_phase_number: int = 0):
        
        self.FILEPATH = filepath
        self.ASPECT_RATIO = aspect_ratio
        self.MAP = map
        self.BOUNTY_COUNT = Constants.BountyCount(bounty_count)
        self.COMPOUNDS_IN_ZONE = compounds_in_zone
        self.BOUNTY1_PHASE_NUMBER = bounty1_phase_number
        self.BOUNTY2_PHASE_NUMBER = bounty2_phase_number
        self.map = Screenshot(self.FILEPATH)
        self.NAME = re.search(r"[^\/]+$", self.FILEPATH).group()

    def testGetMapNameWithText(self):
        return self.map.getMapNameFromText() == self.MAP
    
    def testPhaseDetection(self):
        return self.map.getPhaseNumber(1) == self.BOUNTY1_PHASE_NUMBER and \
               self.map.getPhaseNumber(2) == self.BOUNTY2_PHASE_NUMBER
    
    def testBountyCount(self):
        return self.map.getBountyTotal() == self.BOUNTY_COUNT

        
desalle_16_9_2B = TestMap("tests/testing_images/desalle_16.9_2B.png", 
                          fractions.Fraction(3440, 1440), 
                          Constants.Desalle, 
                          2,
                          2,
                          -1,
                          -1)

stillwater_16_9_1B = TestMap("tests/testing_images/stillwater_16.9_1B.png", 
                             fractions.Fraction(16, 9), 
                             Constants.Stillwater, 
                             1,
                             6,
                             2,
                             -1)

stillwater_21_9_2B = TestMap("tests/testing_images/stillwater_21.9_2B.jpg", 
                             fractions.Fraction(21, 9), 
                             Constants.Stillwater, 
                             2,
                             16,
                             0,
                             0)

desalle_21_9_2B = TestMap("tests/testing_images/desalle_21.9_2B.jpg", 
                          fractions.Fraction(3440, 1440), 
                          Constants.Desalle, 
                          2,
                          16,
                          0,
                          0)

lawson_21_9_2B = TestMap("tests/testing_images/lawson_21.9_2B.jpg", 
                         fractions.Fraction(3440, 1440), 
                         Constants.Lawson, 
                         2,
                         16,
                         0,
                         0)

lawson_21_9_1B = TestMap("tests/testing_images/lawson_21.9_1B.jpg", 
                         fractions.Fraction(3440, 1440), 
                         Constants.Lawson, 
                         1,
                         16,
                         0,
                        -1)

testing_maps = [desalle_16_9_2B,stillwater_16_9_1B,stillwater_21_9_2B,desalle_21_9_2B,lawson_21_9_2B,lawson_21_9_1B ]
