from Map import Map
import Constants
import fractions

class TestMap():
    FILEPATH: str
    ASPECT_RATIO: fractions.Fraction
    MAP: Constants.Map
    BOUNTY_COUNT: int

    def __init__(self, filepath: str, aspect_ratio: fractions.Fraction, map: Constants.Map, bounty_count: int):
        self.FILEPATH = filepath
        self.ASPECT_RATIO = aspect_ratio
        self.MAP = map
        self.BOUNTY_COUNT = bounty_count

desalle_16_9_2B = TestMap("tests/testing_images/desalle_16.9_2B.png", fractions.Fraction(3440, 1440), Constants.Desalle, 2)
stillwater_16_9_1B = TestMap("tests/testing_images/stillwater_16.9_1B.png", fractions.Fraction(16, 9), Constants.Stillwater, 1)
stillwater_21_9_2B = TestMap("tests/testing_images/stillwater_21.9_2B.jpg", fractions.Fraction(21, 9), Constants.Stillwater, 2)
desalle_21_9_2B = TestMap("tests/testing_images/desalle_21.9_2B.jpg", fractions.Fraction(3440, 1440), Constants.Desalle, 2)