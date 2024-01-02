#from image_processing import *
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

"""GOLDEN = (424, 100)
SALTERS = (584, 125)
BLANC = (249, 85)
GODARD = (76, 100)
LAWSON = (265, 181)
ARDEN = (490, 286)
WINDY = (624, 366)
SWEETBELL = (327, 339)
MAW = (114, 269)
NICHOLS = (465, 454)
FORT = (265, 461)
IRON = (75, 427)
WOLFS = (101, 603)
LUMBER = (424, 563)
HEMLOCK = (584, 585)
BRADLEY = (287, 585)

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

LAWSON_FULL_NAMES = {
    "Godard Docks" : GOLDEN,
    "Salter's Pork" : SALTERS,
    "Blanc Brinery" : BLANC,
    "Golden Acres" : GOLDEN,
    "Lawson Station" : LAWSON,
    "Arden Parish" : ARDEN,
    "Windy Run" : WINDY,
    "Sweetbell Flour" : SWEETBELL,
    "Maw Battery" : MAW,
    "Nichols Prison" : NICHOLS,
    "Iron Works" : IRON,
    "Fort Carmick" : FORT,
    "Wolfshead Arsenal" : WOLFS,
    "Bradley & Craven Brickworks" : BRADLEY,
    "C&A Lumber" : LUMBER,
    "Hemlock and Hide" : HEMLOCK
    
    
}"""

"""engine = create_engine('postgresql://happy:password@localhost:5432/hunt', echo = True)
metadata_obj = MetaData()

import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)"""
import sqlalchemy
from sqlalchemy import select, insert

import psycopg2

from constants import Lawson, session
from scheme import Town

engine = create_engine('postgresql://happy:password@localhost:5432/hunt', echo = True)
metadata_obj = MetaData()
if __name__ == "__main__":

    with session:
        session.add_all(Lawson.getTowns())
        
        session.commit()