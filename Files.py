import os,sys
import calendar, time
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Icons:

    def __init__(self,filename):
        self.filename = filename
        self.img = Image.open(filename)
    
    def size(self):
        return self.img.size
    
    @staticmethod
    def read_items(dir):
        files = os.listdir('gfx/'+dir)
        return files

class Drawings:

    def __init__(self,filename):
        self.filename = filename
        self.img = Image.open(filename)
    
    def add_label(self,lettering):
        year = random.randint(1956,1982)
        lettering = "The " + lettering + " House (" + str(year) + ")"
        draw = ImageDraw.Draw(self.img)
        type = ImageFont.truetype("type/GentiumPlus-I.ttf",18)
        w,h = self.img.size
        tw,th = type.getsize(lettering)
        draw.text(
            (w/2 - tw/2,h-50),
            lettering,
            (0,0,0),
            font=type
        )
        self.img.save(self.filename)
        
class Names:

    def __init__(self):
        with open('names/names.list','r') as f:
            names = f.read()
        self.list = names.split("\n")
    
    def choose(self):
        seed = random.randint(0,len(self.list)-1)
        return self.list[seed].lower().title()
