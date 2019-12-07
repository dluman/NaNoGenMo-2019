import random

def orientation((x1,y1),(x2,y2)):
    if x2-x1 == 0:
        return "vertical"
    if y2-y1 == 0:
        return "horizontal"

def place(start,finish):
    if finish > start:
        point = random.uniform(start+20,finish-20)
    else:
        point = random.uniform(start-20,finish+20)
    return point
   
def min_space(start,end):
    if abs(start-end) < 40:
        return False   
    return True

def obj_clear(elements,(x1,y1)):
    for element in elements:
        x,y = element['point']
        if abs(x1-x) < 20 and abs(y1-y) < 20:
            return False
    return True

def contained(elements,point):
    x1,y1 = point
    for element in elements:
        x2,y2 = element['point']
        if abs(x2-x1) < 10 or abs(y2-y1) < 10:
            return True
    return False