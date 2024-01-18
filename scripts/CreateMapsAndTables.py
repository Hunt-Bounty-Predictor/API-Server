from Constants import Maps, session
from scheme import Map
from helpers import getAllInnerClasses
from sqlalchemy.exc import IntegrityError

with session:
    
    for Map in Maps.getMaps():
        try:
            session.add(Map)
            
            session.commit()
            
            
        except IntegrityError:
            session.rollback()
            print(f"Map {Map.name} already exists")
            
    for Map in Maps.__subclasses__():
        for town in Map.getTowns():
            try:
                session.add(town)
                
                session.commit()
                
                
            except IntegrityError:
                session.rollback()
                print(f"Town {town.name} already exists")