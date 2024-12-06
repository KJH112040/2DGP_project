from pico2d import *

import random
import math
import game_framework
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import server

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 2.0  # Km / Hour
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
        self.font = load_font('DungGeunMo.ttf', 24)
        self.build_behavior_tree()

    def get_bb(self):
        return (self.x-server.map.window_left-5,self.y-server.map.window_bottom-5,
                self.x-server.map.window_left+5,self.y-server.map.window_bottom+5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()

    def draw(self):
        if math.cos(self.dir) > 0:
            Monster.images[self.state][int(self.frame)].composite_draw(0, 'h', (self.x-server.map.window_left)*4
                                                                       , (self.y-server.map.window_bottom)*4, 40, 40)
        else:
            Monster.images[self.state][int(self.frame)].draw((self.x-server.map.window_left)*4
                                                                       , (self.y-server.map.window_bottom)*4, 40, 40)
        draw_rectangle((self.x-server.map.window_left-5)*4,(self.y-server.map.window_bottom-5)*4,
                (self.x-server.map.window_left+5)*4,(self.y-server.map.window_bottom+5)*4)
        self.font.draw((self.x-server.map.window_left-6)*4,(self.y-server.map.window_bottom+7)*4,f'HP:{self.hp}',(255,50,50))

    def handle_event(self,event):pass

    def handle_collision(self,group,other):pass

    def set_random_location(self):
        self.tx, self.ty = random.randint(20, 1220), random.randint(20, 840)
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1-x2)**2 + (y1-y2)**2
        return distance2<(PIXEL_PER_METER*r)**2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty-self.y,tx-self.x)
        distance = RUN_SPEED_PPS*game_framework.frame_time
        self.x+=distance*math.cos(self.dir)
        self.y+=distance*math.sin(self.dir)

    def move_to(self, r=0.5):
        self.state='move'
        self.move_slightly_to(self.tx,self.ty)
        if self.distance_less_than(self.tx,self.ty,self.x,self.y,r):
            return BehaviorTree.SUCCESS
        else:
            return  BehaviorTree.RUNNING

    def is_player_nearby(self, distance):
        if self.distance_less_than(server.player.x, server.player.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_player(self, r=0.5):
        self.state='move'
        self.move_slightly_to(server.player.x,server.player.y)
        if self.distance_less_than(server.player.x,server.player.y, self.x,self.y,r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
    
    def build_behavior_tree(self):
        a1 = Action('Set random location',self.set_random_location)
        a2 = Action('Move to',self.move_to)
        a3 = Action('Move to player',self.move_to_player)

        c1 = Condition('player가 근처인가?',self.is_player_nearby,2)

        root = wander = Sequence('Wander',a1,a2)
        root = chase_player = Sequence('player에게 접근', c1, a3)

        root = chase_or_flee = Selector('추격 또는 배회', chase_player,wander)
        self.bt = BehaviorTree(root)