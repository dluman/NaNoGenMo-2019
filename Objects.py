import random,os,sys
import Coordinates as Coord
import Files

from shapely.geometry import Polygon, Point

class Exterior:
    
    def __init__(self,walls):
        self.walls = walls.exterior
        self.doors = self.add_doors()
        self.windows = self.add_windows()
    
    def add_doors(self):
        doors = []
        for i in range(0,len(self.walls.coords)-1):
            x1,y1 = self.walls.coords[i]
            x2,y2 = self.walls.coords[i+1]
            orientation = Coord.orientation(
                (x1,y1),
                (x2,y2)
            )
            if orientation == "horizontal":
                if Coord.min_space(x1,x2):
                    point = (
                        Coord.place(x1,x2),
                        y1
                    )
                    rotate = 90
            if orientation == "vertical":
                if Coord.min_space(y1,y2):
                    point = (
                        x1,
                        Coord.place(y1,y2)
                    )
                    rotate = 0
            if random.randint(0,1):
                doors.append(
                    {
                        'point':point,
                        'rotate':rotate
                    }
                )
            i += 1
        return doors
    
    def add_windows(self):
        windows = []
        for i in range(0,len(self.walls.coords)-1):
            x1,y1 = self.walls.coords[i]
            x2,y2 = self.walls.coords[i+1]
            orientation = Coord.orientation(
                (x1,y1),
                (x2,y2)
            )
            if orientation == "horizontal":
                if Coord.min_space(x1,x2):
                    point = (
                        Coord.place(x1,x2),
                        y1
                    )
                rotate = 90
            if orientation == "vertical":
                if Coord.min_space(y1,y2):
                    point = (
                        x1,
                        Coord.place(y1,y2)
                    )
                    rotate = 0
            if Coord.obj_clear(self.doors,point) and Coord.obj_clear(windows,point):
                windows.append(
                    {
                        'point':point,
                        'rotate':rotate
                    }
                )
            i += 1
        return windows
        
class Interior:
    
    def __init__(self,rooms,exterior):
        self.rooms = rooms
        self.exterior = exterior.exterior
        self.doors = self.add_doors()
        self.items = self.add_room_items()
    
    def add_doors(self):
        doors = []
        for room in self.rooms:
            for i in range(0,len(room['shape'].exterior.coords) - 1):
                x1,y1 = room['shape'].exterior.coords[i]
                x2,y2 = room['shape'].exterior.coords[i+1]
                orientation = Coord.orientation(
                    (x1,y1),
                    (x2,y2)
                )
                if orientation == "horizontal":
                    if Coord.min_space(x1,x2):
                        point = (
                            Coord.place(x1,x2),
                            y1
                        )
                    rotate = 90
                if orientation == "vertical":
                    if Coord.min_space(y1,y2):
                        point = (
                            x1,
                            Coord.place(y1,y2)
                        )
                        rotate = 0
                door_space = Polygon(
                    [
                        point,
                        (point[0]+10,point[1]),
                        (point[0]+10,point[1]+10),
                        (point[0]+10,point[1])
                    ]
                )
                if not door_space.intersects(self.exterior):
                    doors.append(
                        {
                            'point':point,
                            'rotate':rotate
                        }
                    )
                    break
                i += 1
        return doors
    
    @staticmethod
    def check_unique_items(item,items):
        for thing in items:
            if item == thing['file']:
                return False
        return True
    
    def add_room_items(self):
        items = []
        choices = []
        #for room in self.rooms:
        #    type = room['type'].lower()
        #    choices = Files.Icons.read_items(type)
        #    for _ in range(4):
        #        print random.choice(choices)
        for room in self.rooms:
            for i in range(0,len(room['shape'].exterior.coords) - 1):
                x1,y1 = room['shape'].exterior.coords[i]
                x2,y2 = room['shape'].exterior.coords[i+1]
                orientation = Coord.orientation(
                    (x1,y1),
                    (x2,y2)
                )
                if orientation == "horizontal":
                    if Coord.min_space(x1,x2):
                        point = (
                            Coord.place(x1,x2),
                            y1-5
                        )
                    rotate = 0
                    if not Point(point).within(room['shape']):
                        point = (
                            Coord.place(x1,x2),
                            y1+5
                        )
                        rotate = 180
                if orientation == "vertical":
                    if Coord.min_space(y1,y2):
                        point = (
                            x1+5,
                            Coord.place(y1,y2)
                        )
                        rotate = 90
                    if not Point(point).within(room['shape']):
                        point = (
                            x1-5,
                            Coord.place(y1,y2)
                        )
                        rotate = 270
                item_space = Polygon(
                    [
                        point,
                        (point[0]+10,point[1]),
                        (point[0]+10,point[1]+10),
                        (point[0]+10,point[1])
                    ]
                )
                if self.check_unique_items('gfx/study/book1.png',items):
                    for thing in items:
                        if Coord.obj_clear(thing['location'],point):
                            items.append(
                                {
                                    'file':'gfx/study/books1.png',
                                    'size':Files.Icons('gfx/study/books1.png').size(),
                                    'rotate':rotate,
                                    'location':point
                                }
                            )
        return items