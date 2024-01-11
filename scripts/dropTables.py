from scheme import Base
from sqlalchemy import create_engine, MetaData, text
from constants import engine
# Replace 'your_database_uri' with your actual database URI

# Drop all tables

"""run with python3 -m scripts.dropTables"""

def dropTables():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    with engine.connect() as conn:
        for table in reversed(metadata.sorted_tables):
            conn.execute(table.delete())  # Optionally delete data first
            conn.execute(text(f'DROP TABLE "{table.name}" CASCADE;'))
            print(f"Table {table.name} dropped")
            conn.commit()

if __name__ == "__main__":
    dropTables()