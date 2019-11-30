import random
import Rule
import File
import main
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage
import shapely
import cv2

from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.ops import cascaded_union
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.cbook import get_sample_data
from matplotlib.patches import Polygon as plotPoly

class Grammar:

    def __init__(self):
        self.final_shape = None
        self.polygons = []
        self.rooms = []
        self.lines = []
        self.objects = []
        self.external_features = []
        self.interior_features = []
        self.windows = 0
        self.doors = 0
        self.internals = 0
    
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
        for object in self.objects:
            if child.intersects(object):
                return True
        return False
    
    def display(self):
        x,y = None, None
        try:
            x,y = self.final_shape.exterior.xy
        except:
            print "Trying again..."
            self.external_features = []
            main.main()
        fig, ax = plt.subplots()
        ax.plot(x,y,color='black',linewidth=2.0)
        max_x, max_y = max(x), max(y)
        for polygon in self.rooms:
            #if polygon.within(self.final_shape):
            x,y = polygon.exterior.xy
            ax.plot(x,y,color='black',linewidth=1.5)
        ax = self.plot_graphics(ax,max_x,max_y)
        ax = self.plot_furniture(ax,max_x,max_y)
        #ax2.plot()
        #ax2.axis('off')
        plt.axis('off')
        plt.savefig("a_house.png")
        file = File.ImageOps("a_house.png")
        file.add_label("The Ulysses House")
        #for feature in self.interior_features:
        #    file.add_interior_feature(feature[0],feature[1],feature[2])
        #for feature in self.external_features:
        #    file.add_exterior_features(feature)
        plt.show()
    
    def plot_graphics(self,ax,max_x,max_y):
        #ax2 = ax.twinx().twiny()
        for feature in self.external_features:
            fn = get_sample_data('/home/dluman/NGM-2019/icons/'+feature[0]+'.png', asfileobj=False)
            graphic = feature[0]
            img = plt.imread(fn,format='jpeg')
            w,h,a = img.shape
            ratio = float(w)/float(h)
            x,y = feature[1]
            offset_x,offset_y = 0.5,0.5
            if feature[2] == 90: 
                img = np.rot90(img)
            if feature[2] == 180:
                img = np.rot90(img)
                img = np.rot90(img)
                img = np.rot90(img)
            if feature[2] == -180:
                img = np.rot90(img)
                img = np.rot90(img)
            #print max_x, max_y
            w = (max_x/max_y) * w
            h = (max_x/max_y) * h
            #img = cv2.resize(img,dsize=(int(w),int(h)))
            imagebox = OffsetImage(img,zoom=.2)
            imagebox_size = imagebox.get_data().shape[:2]
            imagebox_x = imagebox._dpi_cor*imagebox_size[1]*.2
            imagebox_y = imagebox._dpi_cor*imagebox_size[0]*.2
            w,h,a = img.shape
            aspect = max_x/max_y
            if feature[2] == 90:
                if graphic == "window1":
                    pass
                else:
                    offset_x = .2
            if feature[2] == -90:
                if graphic == "window1":
                    pass
                else:
                    offset_x = .75
            if feature[2] == 180:
                if graphic == "window1":
                    pass
                else:
                    offset_x = .75
            if feature[2] == -180:
                if graphic == "window1":
                    pass
                else:
                    offset_x = -.7
            else:
                if graphic == "window1":
                    pass
                else:
                    offset_y = .75
            imagebox.image.axes = ax
            ab = AnnotationBbox(
                imagebox,
                (x,y),
                frameon=False,
                pad=0,
                box_alignment=(offset_x,offset_y)
            )
            ax.add_artist(ab)
        return ax
            
    def plot_furniture(self,ax,max_x,max_y):
        for feature in self.interior_features:
            fn = get_sample_data('/home/dluman/NGM-2019/icons/'+feature[0]+'.png', asfileobj=False)
            graphic = feature[0]
            x,y = feature[1]
            img = plt.imread(fn,format='jpeg')
            img = scipy.ndimage.interpolation.rotate(img,feature[2])
            imagebox = OffsetImage(img,zoom=.2)
            imagebox.image.axes = ax
            ab = AnnotationBbox(
                imagebox,
                (x,y),
                frameon=False,
                pad=0
            )
            ax.add_artist(ab)
        return ax
    
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
        self.generate_rooms(polygon,random.randint(3,5))
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
        self.generate_rooms(polygon,random.randint(5,8))
        self.polygons.append(polygon)
        count -= 1
        self.generate_child(count, polygon)
        
    def generate_rooms(self, polygon, count):
        room = None
        self.windows = 0
        self.doors = 0
        self.internals = 0
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
        while self.windows < 1 and self.doors < 1:
            print "GENERATING FEATURES FOR ROOM " + str(len(self.rooms) + 1)
            self.generate_external_feature("h","door1",origin,topright)
            self.generate_external_feature("-h","door1",bottomright,bottomleft)
            self.generate_external_feature("v","door1",origin,bottomright)
            self.generate_external_feature("-v","door1",topright,bottomright)
            self.generate_external_feature("h","window1",origin,topright)
            self.generate_external_feature("-h","window1",bottomright,bottomleft)
            self.generate_external_feature("v","window1",origin,bottomright)
            self.generate_external_feature("-v","window1",topright,bottomright)
        while self.internals < 1:
            self.generate_internal_feature("couch1",random.randint(-30,30),polygon)
            self.generate_internal_feature("bed1",random.randint(-30,30),polygon)
            self.generate_internal_feature("bed2",random.randint(-30,30),polygon)
            self.generate_internal_feature("table1",random.randint(-30,30),polygon)
            self.generate_internal_feature("man1",random.randint(-30,30),polygon)
            self.generate_internal_feature("woman1",random.randint(-30,30),polygon)
            self.generate_internal_feature("tv1",random.randint(-30,30),polygon)
            self.generate_internal_feature("piano1",random.randint(-30,30),polygon)
        self.rooms.append(room)
                
        count -= 1
        self.generate_rooms(polygon, count)
    
    def generate_external_feature(self,orientation,element,orig,end):
        orig_x,orig_y = orig
        end_x, end_y = end
        if orig_y == end_y:
            rotate = 0
            if orientation == "-h": rotate=-180
            x = int(random.uniform(orig_x,end_x))
            point = (x,int(orig_y))
        else: 
            y = int(random.uniform(orig_y,end_y))
            point = (int(orig_x), y)
            rotate = 90
            if orientation == "-v": rotate=180
        for feature in self.external_features:
            if abs(point[0] - feature[1][0]) < 15 and abs(point[1] - feature[1][1]) < 15:
                return
        if (orientation == "h" or orientation == "-h") and abs(point[0] - orig_x) > 15 and abs(point[0] - end_x) > 15:
            self.external_features.append((element,point,rotate))
            if element == "door1": self.doors += 1
            if element == "window1": self.windows += 1
        if (orientation == "v" or orientation == "-v") and abs(point[1] - orig_y) > 15 and abs(point[1] - end_y) > 15:
            self.external_features.append((element,point,rotate))
            if element == "door1": self.doors += 1
            if element == "window1": self.windows += 1
    
    def generate_internal_feature(self,element,rotate,room):
        x,y = room.exterior.xy
        # 86.5, 57.5 test data
        w,h = File.ImageOps(element).get_size()
        max_dim = w * .2 if w > h else h * .2
        # object_space = Polygon(
            # [
                # (min(x)+max_dim,max(y)-max_dim),
                # (max(x)-max_dim,max(y)-max_dim),
                # (max(x)-max_dim,min(y)+max_dim),
                # (min(x)+max_dim,min(y)+max_dim)
            # ]
        # )
        object_space = Polygon(
            [
                (min(x),max(y)),
                (max(x),max(y)),
                (max(x),min(y)),
                (min(x),min(y))
            ]
        )
        x,y = object_space.exterior.xy
        point_x = random.uniform(min(x)+max_dim,max(x)-max_dim)
        point_y = random.uniform(min(y)+max_dim,max(y)-max_dim)
        point = (int(point_x),int(point_y))
        object_itself = Polygon(
            [
                (point_x-(.5*max_dim),point_y+(.5*max_dim)),
                (point_x+(.5*max_dim),point_y+(.5*max_dim)),
                (point_x+(.5*max_dim),point_y-(.5*max_dim)),
                (point_x-(.5*max_dim),point_y-(.5*max_dim))
            ]
        )
        if room.contains(object_itself) and not self.get_collision(object_itself):
            print "PLACING FURNITURE"
            self.objects.append(object_itself)
            self.interior_features.append((element,point,rotate))
            self.internals += 1
    
    def generate_outline(self):
        self.final_shape = cascaded_union(self.polygons)