from constants import engine
import subprocess as sp
import os



if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    parent_dir = os.path.dirname(current_dir)

    os.chdir(parent_dir)

    print(os.getcwd())

    #result = sp.call("python3 -m scripts.dropTables".split())

    sp.call("alembic upgrade head".split())

    sp.call("python -m scripts.CreateMapsAndTables".split())