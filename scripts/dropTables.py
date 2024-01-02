from scheme import Base
from sqlalchemy import create_engine, MetaData, text
# Replace 'your_database_uri' with your actual database URI

# Drop all tables

"""run with python3 -m scripts.dropTables"""

if __name__ == "__main__":
    engine = create_engine('postgresql://happy:password@localhost:5432/hunt', echo = True)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    with engine.connect() as conn:
        for table in reversed(metadata.sorted_tables):
            conn.execute(table.delete())  # Optionally delete data first
            conn.execute(text(f'DROP TABLE "{table.name}" CASCADE;'))
            print(f"Table {table.name} dropped")
            conn.commit()