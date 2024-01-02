from image_processing import *
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

from constants import engine, metadata_obj

#engine = create_engine('postgresql://happy:password@localhost:5432/hunt', echo = True)
#metadata_obj = MetaData()

"""with engine.connect() as conn:
    result = conn.execute(text("DROP TABLE IF EXISTS some_table"))
    conn.commit()"""

"""with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()
    
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )"""
    
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
       print("x:", row.x, "y:", row.y)
    
    for x, y in result:
        print("x:", x, "y:", y)
        
    for row in result:
        print(f"x: {row[0]} y: {row[1]}")
        
    for dict_row in result.mappings():
        print(f"x: {dict_row['x']} y: {dict_row['y']}")
        
with engine.connect() as conn:
    result = conn.execute(text('SELECT x, y FROM some_table WHERE y > :y'), {"y": 2})
    
    for row in result:
        print("x:", row.x, "y:", row.y)
        
with Session(engine) as session:
    result = session.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print("x:", row.x, "y:", row.y)
        
"""with engine.connect() as conn:
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 11, "y": 12}, {"x": 13, "y": 14}])
    
    conn.commit()"""
    
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

print(user_table.c.keys())
print(user_table.primary_key)
print(user_table.name)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False), 
    # Dont have to declare type of ForeignKey, inferred from the type of the primary key of the related column
    Column("email_address", String, nullable=False),
)

#metadata_obj.create_all(engine)

from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

print("\n\n\n", Base.metadata)


class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] # Mapped[str | None]
    
    addresses: Mapped[List['Address']] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    
    user: Mapped[User] = relationship(back_populates="addresses")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
Base.metadata.create_all(engine)

some_table = Table("some_table", metadata_obj, autoload_with=engine)

print(some_table.c.keys())



from sqlalchemy import insert

stmt = insert(user_table).values(name = "spongebob", fullname = "Spongebob Squarepants")

print('\n\n\n\n', stmt)

compiled = stmt.compile()

print(compiled.params, compiled, sep = "\n")


with engine.connect() as conn:
    result = conn.execute(stmt)
    
    print(result.inserted_primary_key)
    #conn.commit()
    
with engine.connect() as conn:
    result = conn.execute(insert(user_table), {"name": "sandy", "fullname": "Sandy Cheeks"})
    #conn.commit()
    
with engine.connect() as conn:
    insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
    print(insert_stmt)

























engine.dispose()


from image_processing import *
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

engine = create_engine('postgresql://happy:password@localhost:5432/hunt', echo = True)
metadata_obj = MetaData()

"""with engine.connect() as conn:
    result = conn.execute(text("DROP TABLE IF EXISTS some_table"))
    conn.commit()"""

"""with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()
    
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )"""
    
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
       print("x:", row.x, "y:", row.y)
    
    for x, y in result:
        print("x:", x, "y:", y)
        
    for row in result:
        print(f"x: {row[0]} y: {row[1]}")
        
    for dict_row in result.mappings():
        print(f"x: {dict_row['x']} y: {dict_row['y']}")
        
with engine.connect() as conn:
    result = conn.execute(text('SELECT x, y FROM some_table WHERE y > :y'), {"y": 2})
    
    for row in result:
        print("x:", row.x, "y:", row.y)
        
with Session(engine) as session:
    result = session.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print("x:", row.x, "y:", row.y)
        
"""with engine.connect() as conn:
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 11, "y": 12}, {"x": 13, "y": 14}])
    
    conn.commit()"""
    
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

print(user_table.c.keys())
print(user_table.primary_key)
print(user_table.name)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False), 
    # Dont have to declare type of ForeignKey, inferred from the type of the primary key of the related column
    Column("email_address", String, nullable=False),
)

#metadata_obj.create_all(engine)

from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

print("\n\n\n", Base.metadata)


class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] # Mapped[str | None]
    
    addresses: Mapped[List['Address']] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    
    user: Mapped[User] = relationship(back_populates="addresses")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
Base.metadata.create_all(engine)

some_table = Table("some_table", metadata_obj, autoload_with=engine)

print(some_table.c.keys())



from sqlalchemy import insert

stmt = insert(user_table).values(name = "spongebob", fullname = "Spongebob Squarepants")

print('\n\n\n\n', stmt)

compiled = stmt.compile()

print(compiled.params, compiled, sep = "\n")


with engine.connect() as conn:
    result = conn.execute(stmt)
    
    print(result.inserted_primary_key)
    #conn.commit()
    
with engine.connect() as conn:
    result = conn.execute(insert(user_table), {"name": "sandy", "fullname": "Sandy Cheeks"})
    #conn.commit()
    
with engine.connect() as conn:
    insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
    print(insert_stmt)























engine.dispose()

