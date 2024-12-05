from pico2d import *

import random
import math
import game_framework
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import server

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

animation_names = ['die1', 'hit1','move','stand']

class Monster:
    images = None

    def load_images(self):
        if Monster.images == None:
            Monster.images = {}
            for name in animation_names:
                Monster.images[name] = [load_image("./monster/"+name+"/%d"%i+".png")for i in range(4)]
            Monster.font = load_font('DungGeunMo.ttf',24)

    def __init__(self,x=None,y=None):
        self.x = x if x else random.randint(20,1220)
        self.y = y if y else random.randint(20,840)
        self.load_images()
        self.dir = 0
        self.speed = 0.0
        self.frame = random.randint(0, 3)
        self.state = 'stand'
        self.hp = 50
        self.tx, self.ty =0,0
        self.build_behavior_tree()

    def get_bb(self):pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        if math.cos(self.dir) < 0:
            Monster.images[self.state][int(self.frame)].composite_draw(0, 'h', (self.x-server.map.window_left)*4
                                                                       , (self.y-server.map.window_bottom)*4, 40, 40)
        else:
            Monster.images[self.state][int(self.frame)].draw((self.x-server.map.window_left)*4
                                                                       , (self.y-server.map.window_bottom)*4, 40, 40)

    def handle_event(self,event):pass

    def handle_collision(self,group,other):pass
    
    def build_behavior_tree(self):pass