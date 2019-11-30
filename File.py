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
    
    def add_exterior_features(self,exterior_feature):
        img = Image.open(self.filename)
        door = Image.open('icons/' + exterior_feature[0] + '.png')
        door = door.convert('RGBA')
        door.rotate(exterior_feature[2], Image.NEAREST, expand = 1)
        print "Rotating %d" % exterior_feature[2]
        door = door.resize((50,50),Image.ANTIALIAS)
        for feature in exterior_feature:
            img.paste(door,(exterior_feature[1][0],exterior_feature[1][1]+25))
        img.save(self.filename)
        img.show()
    
    def add_interior_feature(self,feature,point,rotate):
        base = Image.open(self.filename)
        img = Image.open('icons/'+feature+'.png')
        w,h = img.size
        w *= .2
        h *= .2
        img.rotate(rotate, Image.NEAREST, expand = 1)
        img = img.resize((w,h),Image.ANTIALIAS)
        base.paste(img,point)
        base.save(self.filename)
    
    def get_size(self):
        img = Image.open('icons/'+self.filename+'.png')
        return img.size