from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class ImageOps:
    
    def __init__(self,filename):
        self.filename = filename
    
    def add_label(self,lettering):
        img = Image.open(self.filename)
        draw = ImageDraw.Draw(img)
        type = ImageFont.truetype("type/GentiumPlus-I.ttf",18)
        w,h = img.size
        tw,th = type.getsize(lettering)
        draw.text(
            (w/2 - tw/2,h-50),
            lettering,
            (0,0,0),
            font=type
        )
        img.save(self.filename)