from pico2d import *

import random
import math
import game_framework
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import game_world
import server
import item

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
        self.hp = 75
        self.att = 10
        self.de = 10
        self.inv = 0
        self.died_monster = False
        self.tx, self.ty =0,0
        self.font = load_font('DungGeunMo.ttf', 24)
        self.build_behavior_tree()

    def get_bb(self):
        return self.x-5,self.y-5,self.x+5,self.y+5

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if self.inv > 0: self.inv -= 1
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
        if self.hp > 0: self.font.draw((self.x-server.map.window_left-6)*4,(self.y-server.map.window_bottom+7)*4,f'HP:{self.hp}',(255,50,50))

    def handle_event(self,event):pass

    def handle_collision(self,group,other):
        match group:
            case 'attack:monster':
                if server.player.col_attack:
                    if self.inv == 0:
                        self.state = 'hit1'
                        for i in range(len(server.bag)//2):
                            if type(server.bag[i][0])== item.Weapon:
                                if server.bag[i][0].set:
                                    self.hp-=server.bag[i][0].attack // self.de
                        self.inv = 200

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

    def state_check(self, state):
        if state=='hit1' or state =='stand' and self.inv!=0:
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

    def stop_move(self,i):
        if i> 100:
            self.state = 'stand'
        if i > 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def hp_check(self):
        if self.hp <= 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def die(self):
        if self.died_monster==False:
            self.frame=0
            self.died_monster=True
        self.state='die1'
        if self.frame > 3.9:
            game_world.remove_object(self)
            server.monster_count-=1
        if self.state == 'die1':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    
    def build_behavior_tree(self):
        a1 = Action('Set random location',self.set_random_location)
        a2 = Action('Move to',self.move_to)
        a3 = Action('Move to player',self.move_to_player)
        a4 = Action('멈추기',self.stop_move,self.inv)
        a5 = Action('죽음', self.die)

        c1 = Condition('player가 근처인가?',self.is_player_nearby,2)
        c2 = Condition('몬스터 타격',self.state_check, self.state)
        c3 = Condition('die',self.hp_check)

        root = wander = Sequence('Wander',a1,a2)
        root = chase_player = Sequence('player에게 접근', c1, a3)
        root = stop = Sequence('아프면 멈추기', c2, a4)
        root = die = Sequence('죽음',c3,a5)

        root = die_or_stop = Selector('죽었나?맞았나?', die, stop)
        root = stop_or_chase = Selector('쫓을 수 있나', die_or_stop,chase_player)

        root = chase_or_flee = Selector('추격 또는 배회', stop_or_chase,wander)
        self.bt = BehaviorTree(root)