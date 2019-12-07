import random

from shapely.geometry import Polygon

class Coords:
    
    @staticmethod
    def create(origin=(0,0)):
        x,y = origin
        if x == 0 and y ==0:
            scalar = 1.00
        else:
            scalar = random.uniform(.75,1.50)
        offset = -1 if random.randint(0,1) else 1
        coords = [
            origin,
            (x+(100*offset)*scalar,y),
            (x+(100*offset)*scalar,y+(50*offset)*scalar),
            (x,y+(50*offset)*scalar)
        ]
        invert = random.randint(0,1)
        if invert: coords = Coords.reverse(coords)
        return coords
            
    @staticmethod
    def reverse(coords):
        for i in range(len(coords)):
            coords[i] = coords[i][::-1]
        return coords
        
def generate(origin=(0,0)):
    return Coords.create(origin)

if __name__ == '__main__':
    generate()