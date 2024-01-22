
from fractions import Fraction
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Literal, Optional, Tuple
from scheme import Town, Map

HUNT_DATABASE_URL = "postgresql://happy:password@localhost:5432/hunt"

PROD_ENGINE = create_engine(HUNT_DATABASE_URL, echo=True)

def get_db():
    try:
        db = Session(PROD_ENGINE)
        yield db
    finally:
        db.close()

def get_path():
    yield "data/"

engine = create_engine('postgresql://happy:password@localhost:5432/hunt', echo=True)
metadata_obj = MetaData()
session = Session(engine)

class Maps:
    ID = -1
    
    @classmethod
    def getTowns(cls, mapId : int, startId : int = 1) -> List[Town]:
        towns = []
        for town in cls.__dict__.values():
            if isinstance(town, Town):
                
                town.id = startId
                startId += 1
                
                town.map_id = mapId
                
                towns.append(town)

        towns.sort(key=lambda town: town.id)
                
        return towns
    
    @classmethod    
    def getMaps(cls) -> List[Map]:
        maps = []
        for map in cls.__subclasses__():
            maps.append(Map(name=map.NAME, id=map.ID))
            
        return maps
    
    @classmethod
    def getTownTuples(cls) -> List[Tuple[int, int]]:
        return [(town.x, town.y) for town in cls.getTowns()]
    
class Lawson(Maps):
    ID = 2
    NAME = "Lawson Delta"
    PATH = "defaultMaps/lawson.jpg"
    
    GOLDEN = Town(name="Golden Acres", x=424, y=100)
    SALTERS = Town(name="Salter's Pork", x=584, y=125)
    BLANC = Town(name="Blanc Brinery", x=249, y=85)
    GODARD = Town(name="Godard Docks", x=76, y=100)
    LAWSON = Town(name="Lawson Station", x=265, y=181)
    ARDEN = Town(name="Arden Parish", x=490, y=286)
    WINDY = Town(name="Windy Run", x=624, y=366)
    SWEETBELL = Town(name="Sweetbell Flour", x=327, y=339)
    MAW = Town(name="Maw Battery", x=114, y=269)
    NICHOLS = Town(name="Nichols Prison", x=465, y=454)
    FORT = Town(name="Fort Carmick", x=265, y=461)
    IRON = Town(name="Iron Works", x=75, y=427)
    WOLFS = Town(name="Wolfshead Arsenal", x=101, y=603)
    LUMBER = Town(name="C&A Lumber", x=424, y=563)
    HEMLOCK = Town(name="Hemlock and Hide", x=584, y=585)
    BRADLEY = Town(name="Bradley & Craven Brickworks", x=287, y=585)

    @classmethod
    def getTowns(cls, mapId = 2, startId = 16):
        return super().getTowns(mapId, startId)
    
class Stillwater(Maps):
    ID = 3
    NAME = "Stillwater Bayou"
    PATH = "defaultMaps/stillwater.jpg"
    
    ALAINS = Town(name="Alain & Sons Fish", x = 82, y=95)
    REYNARD = Town(name="Reynard Mill", x = 232, y = 87)
    PORT = Town(name="Port Reeker", x = 419, y = 113)
    SCUPPER = Town(name="Scupper Lake", x = 567, y = 85)
    BLANCHETT = Town(name="Blanchett Graves", x = 137, y = 252)
    DARROW = Town(name="Darrow Livestock", x = 321, y = 189)
    ALICE = Town(name="Alice Farm", x = 393, y = 281)
    CHAPEL = Town(name="Chapel of Madonna Noire", x = 576, y = 263)
    LOCKBAY = Town(name="Lockbay Docks", x = 294, y = 322)
    PITCHING = Town(name="Pitching Crematorium", x= 226, y = 479)
    HEALING = Town(name="Healing Waters Church", x = 381, y = 478)
    CYPRESS = Town(name="Cypress Huts", x = 74, y = 543)
    DAVANT = Town(name="Davant Ranch", x = 206, y = 624)
    SLAUGHTER = Town(name="Slaughter House", x = 409, y = 638)
    CATFISH = Town(name="Catfish Grove", x=557, y=585)
    STILLWATER = Town(name = "Stillwater Bend", x = 514, y = 390)
    
    @classmethod
    def getTowns(cls, mapId = 3, startId = 32):
        return super().getTowns(mapId, startId)
    
class Desalle(Maps):
    ID = 1
    NAME = "Desalle"
    PATH = "defaultMaps/desalle.jpg"
    
    KINGSNAKE = Town(name="Kingsnake Mine", x = 79, y = 128)
    COAL = Town(name="Stanley Coal Company", x= 246, y = 126)
    HERITAGE = Town(name="Heritage Pork", x = 404, y = 129)
    PEARL = Town(name="Pearl Plantation", x = 571, y = 127)
    MOSES = Town(name="Moses Poultry", x = 108, y = 298)
    WEEPING = Town(name="Weeping Stone Mill", x = 322, y= 247)
    ASH = Town(name="Ashen Creek Lumber", x = 518, y = 291)
    FORKED = Town(name="Forked River Fishery", x = 354, y = 389)
    SEVEN = Town(name="Seven Sisters Estate", x = 73, y = 417)
    PELICAN = Town(name="Pelican Island Prison", x = 231, y = 417)
    CHURCH = Town(name="First Testimonial Church", x = 473, y = 450)
    UPPER = Town(name="Upper DeSalle", x = 603, y = 382)
    LOWER = Town(name="Lower DeSalle", x = 597, y = 540)
    REEVES = Town(name="Reeves Quarry", x = 443, y = 576)
    DARIN = Town(name="Darin Shipyard", x = 294, y = 596)
    FORT = Town(name = "Fort Bolden", x = 131, y = 560)
    
    @classmethod
    def getTowns(cls, mapId = 1, startId = 0):
        return super().getTowns(mapId, startId)
      
class Crops:
    ULTRAx = 1254
    ULTRAy = 170
    ULTRAwidth = 926
    ULTRAheight = 75

    NORMx = 630
    NORMy = 140
    NORMwidth = 680
    NORMheight = 50
    
    ULTRA_MAP_NAME = (ULTRAx, ULTRAy, ULTRAx + ULTRAwidth, ULTRAy + ULTRAheight)
    NORM_MAP_NAME = (NORMx, NORMy, NORMx + NORMwidth, NORMy + NORMheight)
    NORM_MAP = (600, 190, 600 +  717, 190 + 717)
    ULTRA_MAP = (1240, 255, 1240 + 955, 255 + 955)
    
    ULTRA_BOUNTY_1_NUMS = (139, 130, 139 + 72, 130 + 38)
    ULTRA_BOUNTY_1_PHASE = (74, 82, 74 + 28, 82 + 40)
    
    ULTRA_BOUNTY_2_NUMS = (138, 256, 138 + 72, 256 + 38)
    ULTRA_BOUNTY_2_PHASE = (74, 209, 74 + 31, 209 + 31)
    
    NORMAL_BOUNTY_1_NUMS = (104, 100, 104 + 53, 100 + 23)
    NORMAL_BOUNTY_1_PHASE = (56, 65, 56 + 25, 65 + 25)
    
    NORMAL_BOUNTY_2_NUMS = (100, 195, 100 + 58, 195 + 25)
    NORMAL_BOUNTY_2_PHASE = (53, 156, 53 + 25, 156 + 25)

class Sizes():
    DESIRED_SIZE = (700, 700)
    
class AspectRatio:
    RATIOS = []

    @classmethod
    def getRatios(cls) -> List[Fraction]:
        return cls.RATIOS

class ULTRA_WIDE(AspectRatio):
    RATIOS = [Fraction(21, 9), Fraction(43, 18), Fraction(64, 27)]
    
class NORMAL(AspectRatio):
    RATIOS = [Fraction(16, 9), Fraction(16, 10), Fraction(18, 9), Fraction(19, 10)]
    
from enum import Enum

class CropOptions(Enum):
    MAP = 1
    NAME = 2
    BOUNTY_1_NUMBERS = 3
    BOUNTY_1_PHASE = 4
    BOUNTY_2_NUMBERS = 5
    BOUNTY_2_PHASE = 6
    
class BountyPhases(Enum):
    NO_CLUE = 0
    ONE_CLUE = 1
    TWO_CLUE = 2
    THREE_CLUE = 3
    
class BountyCount(Enum):
    ONE = 1
    TWO = 2
    
import numpy
    
COLORED_IMAGE = numpy.ndarray[Literal[3]]
GRAYSCALE_IMAGE = numpy.ndarray[Literal[2]]

BOUNTY_SYMBOL_THRES = 100