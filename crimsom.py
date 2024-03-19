import sys
import pyMeow as pm
from math import *

try:
    proc = pm.open_process("Crimsonland.exe")
    base = pm.get_module(proc, "Crimsonland.exe")["base"]
    prog = pm.get_module(proc,"prog.dll")["base"]
except Exception as e:
    sys.exit(e)

class Addresses:
    aim_x = base+0x3104A4
    aim_y = base+0x3104A8
    aim_fx = prog+0x201730
    aim_fy = prog+0x201734
    player_x = prog+0x2016C8
    player_y = prog+0x2016CC
    entity_list = prog+0x1A7300
    entity_count = prog+0x18D088
    screen_width = base+0x225C88
    screen_height = base+0x225C8C

class Offsets:
    ent = 0x10C
    x = 0x28
    y = 0x2C
    health = 0x54

class Entity:
    def __init__(self,index):
        self.index = index
        self.base = Addresses.entity_list+Offsets.ent*index
        self.x = self.base+Offsets.x
        self.y = self.base+Offsets.y
        self.h = self.base+Offsets.health
        self.total_health = self.health()

        
    def position(self,x=None,y=None):
        if x is None and y is None:
            return [pm.r_float(proc,self.x),pm.r_float(proc,self.y)]
        else:
            if x is not None:
                pm.w_float(proc,self.x,x)
            if y is not None:
                pm.w_float(proc,self.y,y)
    def health(self,h=None):
        if h is None:
            return pm.r_float(proc,self.h)
        else:
            pm.w_float(proc,self.h,h)

def entities():
    n_entities = pm.r_int(proc,Addresses.entity_count)
    ents = []
    i=0
    while i!= n_entities:
        is_valid = not pm.r_int(proc,Addresses.entity_list+Offsets.ent*i) == 1
        if is_valid:
            ents.append(Entity(i))
        i+=1
    return ents

def distance(A,B):
    return sum([(B[i]-A[i])**2 for i in range(2)])

def screen_dimentions():
    return [pm.r_int(proc,Addresses.screen_width),pm.r_int(proc,Addresses.screen_height)]

def aimcoors(x=None,y=None):
    if x is None and y is None:
        x = pm.r_int(proc,Addresses.aim_x)
        y = pm.r_int(proc,Addresses.aim_y)
        return [x,y]
    else:
        if x is not None:
            pm.w_int(proc,Addresses.aim_x,x)
        if y is not None:
            pm.w_int(proc,Addresses.aim_y,y)

def player_position(x=None,y=None):
    if x is None and y is None:
        return [pm.r_float(proc,Addresses.player_x),pm.r_float(proc,Addresses.player_y)]
    else:
        if x is not None:
            pm.w_float(proc,Addresses.player_x,x)
        if y is not None:
            pm.w_float(proc,Addresses.player_y,y)

def teleport_tocrosshair(ents):
    tx,ty = aimcoors()
    px,py = player_position()
    width,height = screen_dimentions()
    px+=tx-width/2
    py+=ty-height/2
    for i in ents:
        i.position(x=px,y=py)

def get_distance(vector1, vector2):
    distance = sqrt((vector2[0] - vector1[0])**2 + (vector2[1] - vector1[1])**2)
    return distance

def closest_ent(ents):
    ply_pos = player_position()
    min_dist = get_distance(ply_pos,ents[0].position())
    min_ent = ents[0]
    for i in ents[1:]:
        dist = get_distance(ply_pos,i.position())
        if  dist < min_dist:
            min_dist = dist
            min_ent = i
    return min_ent

def aim_toent(closest_entity):
    entity_x, entity_y = closest_entity.position()
    screen_width, screen_height = screen_dimentions()
    player_x, player_y = player_position()
    aim_x = int((entity_x - player_x) + screen_width / 2)
    aim_y = int((entity_y - player_y) + screen_height / 2)
    aimcoors(x=aim_x, y=aim_y)


def main():
    while True:          
        ents = entities()
        if len(ents) >0:
            close_ent = closest_ent(ents)
            aim_toent(close_ent)
        
        



if __name__ == "__main__":
    main()