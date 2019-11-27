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
    def get_size(x_val,y_val):
        max = x_val[0]
        for x in x_val:
            if x > max:
                max = x
                w = x
        max = y_val[0]
        for y in y_val:
            if y > max:
                max = y
                h = y
        return (w,h)
    
    @staticmethod
    def choose_origin(x,y):
        rand = 1
        while rand % 2 != 0:
            rand = random.randint(0,10)
        if rand == 0:
            rand = 1
        return (x/rand,y/rand)
        
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
        plt.plot(x,y,color='black')
        #for line in self.lines:
        #    print line
        #    plt.plot(
        #        [line[0][0],
        #        line[0][1]],
        #        [line[1][0],
        #        line[1][1]],
        #        color='black'
        #    )
        for polygon in self.rooms:
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
        #self.generate_walls(polygon,random.randint(0,1))
        self.polygons.append(polygon)
    
    def generate_child(self, count, previous = None):
        orientation = self.lateral()
        if count == 0:
            return
        if previous:
            latest = previous
        else:
            latest = self.polygons[len(self.polygons) - 1]
        x_val, y_val = latest.exterior.xy
        w, h = self.get_size(x_val,y_val)
        x, y = self.choose_origin(w,h)
        if orientation:
            polygon = Polygon(
                [
                    (x,y),
                    (x+100,y),
                    (x+100,y+50),
                    (x,y+50)
                ]
            )
        else:
            polygon = Polygon(
                [
                    (x,y),
                    (x,y+100),
                    (x+50,y+100),
                    (x+50,y)
                ]
            )
        #self.generate_walls(polygon,random.randint(0,1))
        self.generate_rooms(polygon,random.randint(0,1))
        self.polygons.append(polygon)
        count -= 1
        self.generate_child(count, polygon)
        
    def generate_rooms(self, polygon, count):
        if count == 0: return
        room = None
        x_vals, y_vals = polygon.exterior.xy
        _x = min(x_vals)
        orig_x = _x
        _y = random.uniform(min(y_vals),max(y_vals))
        orig_y = _y
        
        origin = (_x,_y)
        
        while Point(_x+1,_y).within(polygon):
            _x += 1
        _x += 1
        topright = (_x,_y)
                
        _x = orig_x
        while Point(_x+1,_y-1).within(polygon):
            _y -= 1
        bottomleft = (_x,_y)
                
        _x = max(x_vals)
        _y = orig_y
        while Point(_x-1,_y-1).within(polygon):
            _y -= 1
        bottomright = (_x,_y)
        orientation = self.lateral()
        if orientation:
            room = Polygon(
                [
                    origin,
                    topright,
                    bottomright,
                    bottomleft
                ]
            )
        else:
            room = Polygon(
                [
                    origin[::-1],
                    topright[::-1],
                    bottomright[::-1],
                    bottomleft[::-1]
                ]
            )
        
        if self.get_collision(room):
            return
            
        self.rooms.append(room)
                
        count -= 1
        self.generate_rooms(polygon, count)
        
    def generate_walls(self, polygon, count):
        if count == 0:
            return
        line = []
        x_val, y_val = polygon.exterior.xy
        orientation = self.lateral()
        #_x = random.uniform(min(x_val),max(x_val))
        orig_x = min(x_val)
        _x = orig_x
        orig_y = random.uniform(min(y_val),max(y_val))
        _y = orig_y
        while Point(_x+1,_y).within(polygon):
            line.append((_x,_y))
            _x += 1
        _x += 1
        line.append((_x,_y))
        wall = ([line[0][0],line[len(line)-1][0]],
                [line[0][1],line[len(line)-1][1]])
        line = []
        self.lines.append(wall)
        _x = orig_x
        while Point(_x+1,_y).within(polygon):
            line.append((_x,_y))
            _y -= 1
        wall = ([line[0][0],line[len(line)-1][0]],
                [line[0][1],line[len(line)-1][1]])
        line = []
        self.lines.append(wall)
        _x = max(x_val)
        _y = orig_y
        while Point(_x-1,_y).within(polygon):
            line.append((_x,_y))
            _y -= 1
        wall = ([line[0][0],line[len(line)-1][0]],
                [line[0][1],line[len(line)-1][1]])
        self.lines.append(wall)
        line = []
        _x = orig_x
        _y = min(y_val)
        while Point(_x+1,_y+1).within(polygon):
            line.append((_x,_y))
            _x += 1
        _x += 1
        line.append((_x,_y))
        wall = ([line[0][0],line[len(line)-1][0]],
                [line[0][1],line[len(line)-1][1]])
        self.lines.append(wall)
        count -= 1
        self.generate_walls(polygon, count)
    
    def generate_outline(self):
        self.final_shape = cascaded_union(self.polygons)