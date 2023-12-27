
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional


class Base(DeclarativeBase):
    pass

#https://alembic.sqlalchemy.org/en/latest/tutorial.html

#alembic revision --autogenerate -m ""
#alembic upgrade head

"""class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] # Mapped[str | None]
    
    addresses: Mapped[List['Address']] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"""
    
class Map(Base):
    __tablename__ = "map"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    towns: Mapped[List['Town']] = relationship(back_populates="map")
    extracts: Mapped[List['Extract']] = relationship(back_populates="map")
    phases: Mapped[List['Phase']] = relationship("Phase", back_populates="what_map")
    
    def __repr__(self) -> str:
        return f"Map(id={self.id!r}, name={self.name!r})"
    
class Town(Base):
    __tablename__ = "town"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"))
    map: Mapped[Map] = relationship(back_populates="towns")
    
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
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"
    
    
class Image(Base):
    __tablename__ = "image"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="images")
    
    path: Mapped[str]
    phase: Mapped[Optional['Phase']] = relationship(back_populates="image")
    
    def __repr__(self) -> str:
        return f"Image(id={self.id!r}, name={self.name!r}"
    
class Phase(Base):
    __tablename__ = "phase"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    image_id: Mapped[int] = mapped_column(ForeignKey("image.id"))
    image: Mapped[Image] = relationship(back_populates="phase")
    
    
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"))  # Foreign key to Map
    what_map: Mapped[Map] = relationship("Map", back_populates="phases")  # Relationship to Map
    
    phase_number: Mapped[int]
    towns: Mapped[str] = mapped_column(String(16))
    
    def __repr__(self) -> str:
        return f"Phase(id={self.id!r}, name={self.name!r}"