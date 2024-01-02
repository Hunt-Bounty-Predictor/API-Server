
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Literal, Optional, Tuple
from scheme import Town, Map

engine = create_engine('postgresql://happy:password@localhost:5432/hunt')
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
      
class Crops:
    ULTRAx = 1254
    ULTRAy = 170
    ULTRAwidth = 926
    ULTRAheight = 75

    NORMx = 608
    NORMy = 115
    NORMwidth = 699
    NORMheight = 71
    
    ULTRA_MAP_NAME = (ULTRAx, ULTRAy, ULTRAx + ULTRAwidth, ULTRAy + ULTRAheight)
    NORM_MAP_NAME = (NORMx, NORMy, NORMx + NORMwidth, NORMy + NORMheight)
    NORM_MAP = (600, 190, 600 +  720, 190 + 720)
    ULTRA_MAP = (1240, 255, 1240 + 950, 255 + 950)
    
    ULTRA_BOUNTY_1_NUMS = (139, 130, 139 + 72, 130 + 38)
    ULTRA_BOUNTY_1_PHASE = (74, 82, 74 + 28, 82 + 40)
    
    ULTRA_BOUNTY_2_NUMS = (138, 256, 138 + 72, 256 + 38)
    ULTRA_BOUNTY_2_PHASE = (74, 209, 74 + 31, 209 + 31)
    
    DESIRED_SIZE = (700, 700)
    
from enum import Enum

class CropOptions(Enum):
    MAP = 1
    NAME = 2
    BOUNTY_1_NUMBERS = 3
    BOUNTY_1_NAME = 4
    BOUNTY_2_NUMBERS = 5
    BOUNTY_2_NAME = 6
    
class BountyPhases(Enum):
    NO_CLUES = 0
    ONE_CLUE = 1
    TWO_CLUES = 2
    THREE_CLUES = 3
    
import numpy
    
COLORED_IMAGE = numpy.ndarray[Literal[3]]
GRAYSCALE_IMAGE = numpy.ndarray[Literal[2]]
    
    
#print(Lawson.getTowns())
#print(Maps.getMaps())