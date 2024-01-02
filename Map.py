from image_processing import *

class Map:
    def __init__(self, file : str):
        self.file = file
        self.image = loadImage(file, False)
        self.map = getMap(file)
        self.mapName = getMapName(self.image)
        self.maskedMap = getMaskedMap(self.map)
        
if __name__ == "__main__":
    m = Map(r'/mnt/e/replays/Hunt Showdown/Map/testing/images/Lawson 1C.jpg')
    print(m.mapName)