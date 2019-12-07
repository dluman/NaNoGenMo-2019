import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage
import Files

from PIL import Image
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)

import time

def make(outline,rooms,doors,windows,items):
    fig,ax = plt.subplots()
    x,y = outline.exterior.xy
    ax.plot(x,y,color='black',linewidth=3.0)
    for room in rooms:
        x,y = room['shape'].exterior.xy
        ax.plot(x,y,color='black',linewidth=2.0)
    for door in doors:
        x,y = door['point']
        img = np.zeros([13,8,3],dtype=np.uint8)
        if door['rotate'] > 0: img = img = np.zeros([8,13,3],dtype=np.uint8)
        img[0:256,0:256] = [255,255,255]
        imgbox = OffsetImage(img,zoom=1.0)
        imgbox.image.axes = ax
        ab = AnnotationBbox(
            imgbox,
            (x,y),
            frameon=False,
            pad=0,
            box_alignment=(0.5,0.5)
        )
        ax.add_artist(ab)
    for window in windows:
        x,y = window['point']
        img = np.zeros([10,1,3],dtype=np.uint8)
        if window['rotate'] > 0: img = np.zeros([1,10,3],dtype=np.uint8)
        img[0:256,0:256] = [255,255,255]
        imgbox = OffsetImage(img,zoom=1.0)
        imgbox.image.axes = ax
        ab = AnnotationBbox(
            imgbox,
            (x,y),
            frameon=True,
            pad=0,
            box_alignment=(0.5,0.5)
        )
        ax.add_artist(ab)
    for item in items:
        w, h = item['size']
        x,y = item['location']
        img = plt.imread(item['file'])
        if item['rotate'] > 0: img = scipy.ndimage.interpolation.rotate(img,item['rotate'])
        imgbox = OffsetImage(img,zoom=.2)
        imgbox.image.axes = ax
        ab = AnnotationBbox(
            imgbox,
            (x,y),
            frameon=False,
            pad=0,
            box_alignment=(0.5,0.5)
        )
        ax.add_artist(ab)
    plt.axis('off')
    ms = int(round(time.time() * 1000))
    plt.savefig('img/'+str(ms)+'.png')
    name = Files.Names().choose()
    Files.Drawings('img/'+str(ms)+'.png').add_label(name)
    plt.close()