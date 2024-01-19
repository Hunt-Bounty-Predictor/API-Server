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
                 compounds_in_zone: int = 0,
                 bounty1_phase_number: int = 0,
                 bounty2_phase_number: int = -1,
                 name_covered: bool = False):
        
        self.FILEPATH = filepath
        self.ASPECT_RATIO = aspect_ratio
        self.MAP = map
        self.COMPOUNDS_IN_ZONE = compounds_in_zone
        self.BOUNTY1_PHASE_NUMBER = bounty1_phase_number
        self.BOUNTY2_PHASE_NUMBER = bounty2_phase_number
        self.map = Screenshot(self.FILEPATH)
        self.NAME = re.search(r"[^\/]+$", self.FILEPATH).group()
        self.NAME_COVERED = name_covered
        
        self.BOUNTY_COUNT = sum([1 for x in [self.BOUNTY1_PHASE_NUMBER, self.BOUNTY2_PHASE_NUMBER] if x != -1])

    def testGetMapNameWithText(self):
        return self.map.getMapNameFromText() == self.MAP, f"Expected: {self.MAP}, Actual: {self.map.getMapNameFromText()}"
    
    def testPhaseDetection(self):
        return self.map.getPhaseNumber(1) == self.BOUNTY1_PHASE_NUMBER and \
               self.map.getPhaseNumber(2) == self.BOUNTY2_PHASE_NUMBER , f"Expected: {self.BOUNTY1_PHASE_NUMBER}, {self.BOUNTY2_PHASE_NUMBER}, Actual: {self.map.getPhaseNumber(1)}, {self.map.getPhaseNumber(2)}"
    
    def testBountyCount(self):
        return self.map.getBountyTotal() == self.BOUNTY_COUNT, f"Expected: {self.BOUNTY_COUNT}, Actual: {self.map.getBountyTotal()}"

    def checkBountySymbol(self):
        b1 = self.map.checkBountySymbol()
        b2 = self.map.checkBountySymbol(2)
        
        b1IsCorrect = self.BOUNTY1_PHASE_NUMBER != -1
        b2IsCorrect = self.BOUNTY2_PHASE_NUMBER != -1
        
        return b1 == b1IsCorrect and b2 == b2IsCorrect, f"Expected: {b1IsCorrect}, {b2IsCorrect}, Actual: {b1}, {b2}"
    
    def getMapNameFromImage(self):
        return self.map.getMapNameFromImage() == self.MAP, f"Expected: {self.MAP}, Actual: {self.map.getMapNameFromImage()}"
    
    def getMapName(self):
        return self.map.getMapName() == self.MAP, f"Expected: {self.MAP}, Actual: {self.map.getMapName()}"
    
    def getCompundCount(self):
        return self.map.getCompoundCountInBounty(self.map.getMapName().getTownTuples()) == self.COMPOUNDS_IN_ZONE, f"Expected: {self.COMPOUNDS_IN_ZONE}, Actual: {self.map.getCompoundCountInBounty(self.map.getMapName().getTownTuples())}"

    def getMapNameFromText(self):
        map = self.map.getMapNameFromText()
        
        if map == self.MAP or (not map and self.NAME_COVERED):
            return True, f"Expected: {self.MAP}, Actual: {map}"
        
    def isUltra(self):
        isUltra = self.map.isUltra()
        
        if isUltra and self.ASPECT_RATIO in Constants.ULTRA_WIDE.getRatios():
            return True, f"Expected: True, Actual: {isUltra}"
        
        return False, f"Expected: True, Actual: {isUltra}"
        
        
desalle_16_9_2B = TestMap("tests/testing_images/desalle_16.9_2B.png", 
                          fractions.Fraction(3440, 1440), 
                          Constants.Desalle, 
                          2,
                          3,
                          3)

stillwater_16_9_1B = TestMap("tests/testing_images/stillwater_16.9_1B.png", 
                             fractions.Fraction(16, 9), 
                             Constants.Stillwater, 
                             6,
                             2,
                             -1)

stillwater_21_9_2B = TestMap("tests/testing_images/stillwater_21.9_2B.jpg", 
                             fractions.Fraction(21, 9), 
                             Constants.Stillwater, 
                             16,
                             0,
                             0)

desalle_21_9_2B = TestMap("tests/testing_images/desalle_21.9_2B.jpg", 
                          fractions.Fraction(3440, 1440), 
                          Constants.Desalle, 
                          16,
                          0,
                          0)

lawson_21_9_2B = TestMap("tests/testing_images/lawson_21.9_2B.jpg", 
                         fractions.Fraction(3440, 1440), 
                         Constants.Lawson, 
                         16,
                         0,
                         0)

lawson_21_9_1B = TestMap("tests/testing_images/lawson_21.9_1B.jpg", 
                         fractions.Fraction(3440, 1440), 
                         Constants.Lawson, 
                         16,
                         0,
                        -1)

#diff sized images

desalle_21_9_hd_covered = TestMap("tests/different_sized_images/desalle_21.9_HD_text_coverd.jpg",
                                    fractions.Fraction(3440, 1440),
                                    Constants.Desalle,
                                    11,
                                    0,
                                    2,
                                    True)

desalle_21_9_hd = TestMap("tests/different_sized_images/desalle_21.9_HD.jpg",
                                    fractions.Fraction(3440, 1440),
                                    Constants.Desalle,
                                    16,
                                    0,
                                    0)

lawson_21_9_hd = TestMap("tests/different_sized_images/lawson_21.9_HD.jpg",
                                    fractions.Fraction(3440, 1440),
                                    Constants.Lawson,
                                    16,
                                    0,
                                    0)

stillwater_21_9_hd_covered = TestMap("tests/different_sized_images/stillwater_21.9_HD_text_coverd.jpg",
                                    fractions.Fraction(3440, 1440),
                                    Constants.Stillwater,
                                    11,
                                    1,
                                    -1,
                                    True)

stillwater_21_9_HD = TestMap("tests/different_sized_images/stillwater_21.9_HD.jpg",
                                    fractions.Fraction(3440, 1440),
                                    Constants.Stillwater,
                                    16,
                                    0,
                                    0)

diff_sized_images = [desalle_21_9_hd_covered, desalle_21_9_hd, lawson_21_9_hd, stillwater_21_9_hd_covered, stillwater_21_9_HD]
normal_images = [desalle_16_9_2B,stillwater_16_9_1B,stillwater_21_9_2B,desalle_21_9_2B,lawson_21_9_2B,lawson_21_9_1B]

testing_maps = normal_images + diff_sized_images
