import random
import Rule
import File
import main
import matplotlib.pyplot as plt

from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.ops import cascaded_union

class Grammar:

    def __init__(self):
        self.final_shape = None
        self.polygons = []
        self.rooms = []
        self.lines = []
    
    @staticmethod
    def lateral():
        rand = random.randint(0,1)
        if rand > 0:
            return True
        return False
    
    @staticmethod
    def choose_origin(x_val,y_val):
        x_seed = random.randint(0,1)
        y_seed = random.randint(0,1)
        if x_seed: origin_x = max(x_val)
        else: origin_x = min(x_val)
        if y_seed: origin_y = max(y_val)
        else: origin_y = min(y_val)
        return origin_x,origin_y
        
    def get_collision(self, child = None):
        for shape in self.rooms:
            if child.intersects(shape):
                return True
        return False
    
    def display(self):
        try:
            x,y = self.final_shape.exterior.xy
        except AttributeError:
            print "Trying again..."
            main.main()
        plt.plot(x,y,color='black',linewidth=3.0)
        for polygon in self.rooms:
            #if polygon.within(self.final_shape):
            x,y = polygon.exterior.xy
            plt.plot(x,y,color='black')
        plt.axis('off')
        plt.savefig("a_house.png")
        file = File.ImageOps("a_house.png")
        file.add_label("The Ulysses House")
        plt.show()
    
    def generate_parent(self):
        orientation = self.lateral()
        if orientation:
           polygon = Polygon(
            [
                (0,0),
                (100,0),
                (100,50),
                (0,50)
            ]
           )
        else:
           polygon = Polygon(
            [
                (0,0),
                (0,100),
                (50,100),
                (50,0)
            ]
           )
        self.generate_rooms(polygon,random.randint(1,5))
        self.polygons.append(polygon)
    
    def generate_child(self, count, previous = None):
        orientation = self.lateral()
        rule = Rule.Rule()
        if count == 0:
            return
        if previous:
            latest = previous
        else:
            latest = self.polygons[len(self.polygons) - 1]
        x_val, y_val = latest.exterior.xy
        x, y = self.choose_origin(x_val,y_val)
        if orientation:
            polygon = Polygon(
                [
                    (x,y),
                    (x+100*rule.scale_factor,y),
                    (x+100*rule.scale_factor,y+50*rule.scale_factor),
                    (x,y+50*rule.scale_factor)
                ]
            )
        else:
            polygon = Polygon(
                [
                    (x,y),
                    (x,y+100*rule.scale_factor),
                    (x+50*rule.scale_factor,y+100*rule.scale_factor),
                    (x+50*rule.scale_factor,y)
                ]
            )
        self.generate_rooms(polygon,random.randint(1,5))
        self.polygons.append(polygon)
        count -= 1
        self.generate_child(count, polygon)
        
    def generate_rooms(self, polygon, count):
        room = None
        
        if count == 0: return
        
        rule = Rule.Rule()
        scale = rule.scale_factor * 10
        
        x_vals, y_vals = polygon.exterior.xy
        
        _x = min(x_vals) #+ scale
        #_y = y_vals[random.randint(0,len(y_vals)-1)]
        _y = max(y_vals) #- scale
        
        orig_x, orig_y = _x+.1,_y-.1
        
        origin = (_x,_y)
        
        #TOP RIGHT
        while Point(_x+.1,_y-.1).within(polygon):
            _x += .1
        topright = (_x,_y)
                
        #BOTTOM LEFT
        _x = orig_x
        while Point(_x+.1,_y-.1).within(polygon):
            _y -= .1
        bottomleft = (_x,_y)
                
        #BOTTOM RIGHT
        wall_chance = random.randint(0,1)
        if wall_chance:
            _x = orig_x
        else: 
            _x = max(x_vals) - .1
        _y = orig_y
        while Point(_x-.1,_y-.1).within(polygon):
            _y -= .1
        bottomright = (_x,_y)
        
        room = Polygon(
            [
                origin,
                topright,
                bottomright,
                bottomleft
            ]
        )
        
        if self.get_collision(room):
            return
            
        self.rooms.append(room)
                
        count -= 1
        self.generate_rooms(polygon, count)
    
    def generate_outline(self):
        self.final_shape = cascaded_union(self.polygons)