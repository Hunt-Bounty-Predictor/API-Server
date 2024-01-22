
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional


class Base(DeclarativeBase):
    pass

#https://alembic.sqlalchemy.org/en/latest/tutorial.html

#alembic revision --autogenerate -m ""
#alembic upgrade head


class Map(Base):
    __tablename__ = "map"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    towns: Mapped[List['Town']] = relationship(back_populates="map")
    extracts: Mapped[List['Extract']] = relationship(back_populates="map")
    phases: Mapped[List['PrimaryPhase']] = relationship(back_populates="what_map")
    
    def __repr__(self) -> str:
        return f"Map(id={self.id!r}, name={self.name!r})"
    
class Town(Base):
    __tablename__ = "town"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"))
    map: Mapped[Map] = relationship(back_populates="towns")
    
    x: Mapped[int]
    y: Mapped[int]
    
    def __repr__(self) -> str:
        return f"Town(id={self.id!r}, name={self.name!r})"
    
class Extract(Base):
    __tablename__ = "extract"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"))
    map: Mapped[Map] = relationship(back_populates="extracts")
    
    def __repr__(self) -> str:
        return f"Extract(id={self.id!r}, name={self.name!r})"
    
    


class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  = mapped_column(unique=True)
    images: Mapped[List['Image']] = relationship(back_populates="user")
    
    primary_phases: Mapped[List['PrimaryPhase']] = relationship(back_populates="user")
    
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"
    

    
class Image(Base):
    __tablename__ = "image"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="images")
    
    path: Mapped[str] # You do not need the actual file name as it will be the id.
    
    is_primary: Mapped[bool] = mapped_column(default=False)
    phase: Mapped[Optional['Phase']] = relationship(back_populates="image") 
    primary_phase: Mapped[Optional['PrimaryPhase']] = relationship(back_populates="image")
    
    
    def __repr__(self) -> str:
        return f"Image(id={self.id!r}, name={self.name!r}"
    
    
class PrimaryPhase(Base):
    """
    This is the phase that encapsulates the start of the map.
    This will be when no clues have been collected.
    "Round" may never be finished."""
    __tablename__ = "primary_phase"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"))  # Foreign key to Map
    what_map: Mapped[Map] = relationship("Map", back_populates="phases")  # Relationship to Map
    phases: Mapped[List['Phase']] = relationship("Phase", back_populates="primary_phase")
    processingCompleted: Mapped[bool] = mapped_column(default=False)
    
    bounty_count: Mapped[int] = mapped_column(default=1) # only needed in primary phase, all other phases on the same map will have the same number of bounties
    
    image_id: Mapped[int] = mapped_column(ForeignKey("image.id"))
    image: Mapped[Image] = relationship(back_populates="primary_phase")
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="primary_phases")
    
    
class Phase(Base):
    """
    These phases encapsulate all clues coillected from a round. 
    And will ideally have the boss location within on or two of the maps."""
    __tablename__ = "phase"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    image_id: Mapped[int] = mapped_column(ForeignKey("image.id"))
    image: Mapped[Image] = relationship(back_populates="phase")
    
    
    """map_id: Mapped[int] = mapped_column(ForeignKey("map.id"))  # Foreign key to Map
    what_map: Mapped[Map] = relationship("Map", back_populates="phases")  # Relationship to Map
    """
    
    primary_phase_id: Mapped[int] = mapped_column(ForeignKey("primary_phase.id"), index=True)
    primary_phase: Mapped[PrimaryPhase] = relationship("PrimaryPhase", back_populates="phases")
    
    phase_number: Mapped[int]
    towns: Mapped[str] = mapped_column(String(16), default="0000000000000000")
    processingCompleted: Mapped[bool] = mapped_column(default=False)
    
    def __repr__(self) -> str:
        return f"Phase(id={self.id!r}, name={self.name!r}"