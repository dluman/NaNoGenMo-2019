import Rules

import random

from shapely.geometry import Polygon, MultiPolygon

class Kitchen:
    
    def __init__(self):
        self.display_name = "Kitchen"

class LivingRoom:
    
    def __init__(self):
        self.display_name = "Living Room"

class Bedroom:
    
    def __init__(self):
        self.display_name = "Bedroom"

class Study:
    
    def __init__(self):
        self.display_name = "Study"

class CarPort:
    
    def __init__(self):
        self.display_name = "Car Port"

class Blueprint:
    def __init__(self,coords):
        self.types = [
            "Kitchen",
            "LivingRoom",
            "Bedroom",
            "Study",
            "EntryWay"
        ]
        self.area = Polygon(
            coords
        )
        self.lateral = random.randint(0,1)
           
    def generate(self):
        room = {}
        room['type'] = self.types[
            random.randint(0,len(self.types)-1)
        ]
        room['shape'] = Polygon(
            [
                (x,y) for (x,y) in self.area.exterior.coords
            ]
        )
        return room