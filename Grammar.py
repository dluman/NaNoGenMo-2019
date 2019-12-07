import Rules
import Files
import Plot
import Room
import Objects

import random

from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.ops import cascaded_union
from shapely.ops import snap

class History:

    def __init__(self):
        self.walls = []
        self.rooms = []
        self.doors = []
        self.items = []
    
    def add_rule(self,rule):
        wall = Polygon(
            rule
        )
        self.walls.append(wall)
    
    def add_room(self,rule):
        shape = Polygon(
            rule['shape']
        )
        self.rooms.append(
            {
                'type':rule['type'],
                'shape': shape
            }
        )
    
    def add_exterior_features(self,exterior):
        objects = Objects.Exterior(exterior)
        self.doors = objects.doors
        self.windows = objects.windows
    
    def add_interior_features(self,exterior):
        objects = Objects.Interior(self.rooms,exterior)
        self.doors += objects.doors
        self.items = objects.items

def origin(wall):
    x,y = wall.exterior.xy
    if random.randint(0,1):
        x,y = max(x),min(y)
    else:
        x,y = min(x),max(y)
    return x, y
    
def outline(grammar):
    return cascaded_union(grammar.walls)

def check_boundaries(room,rooms):
    for space in rooms:
        if room.intersects(space['shape']):
            return cascaded_union([space['shape'],room])
    return room

def main():
    grammar = History()
    rule = Rules.generate()
    grammar.add_rule(rule)
    room = Room.Blueprint(rule).generate()
    grammar.add_room(room)
    for _ in range(3,random.randint(4,10)):
        walls = grammar.walls
        rule = Rules.generate(
            origin(walls[-1])
        )
        grammar.add_rule(rule)
        room = Room.Blueprint(rule).generate()
        room['shape'] = check_boundaries(
            room['shape'],
            grammar.rooms
        )
        grammar.add_room(room)
    exterior = outline(grammar)
    if exterior.geom_type == 'MultiPolygon':
        main()
    else:
        grammar.add_exterior_features(exterior)
        grammar.add_interior_features(exterior)
        Plot.make(exterior,grammar.rooms,grammar.doors,grammar.windows,grammar.items)

if __name__=='__main__':
    main()