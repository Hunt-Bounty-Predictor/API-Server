from Constants import Maps, session
from scheme import Map
from helpers import getAllInnerClasses
from sqlalchemy.exc import IntegrityError

with session:
    
    for map in Maps.getMaps():
        try:
            session.add(map)
            
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Map {map.name} already exists")