from constants import Maps, session
from scheme import Map
from helpers import getAllInnerClasses

with session:
    for c in getAllInnerClasses(Maps):
        try:
            session.add(Map(name=c.__name__, id=c.id))
            
            session.commit()
        except:
            session.rollback()
            print(f"Map {c.__name__} already exists")