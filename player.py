import math

from pico2d import load_image, load_font, get_canvas_width, get_canvas_height, clamp, draw_rectangle

import server
import game_framework
from state_machine import StateMachine, time_out, space_down, right_down, left_up, left_down, right_up, start_event, \
     attact_end, upkey_down, downkey_down, upkey_up,downkey_up


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION=0.3
ACTION_PER_TIME=1.0/TIME_PER_ACTION
FRAMES_PER_ACTION=4

class Player:
    image=None
    def __init__(self):
        self.frame=0
        self.action=7
        self.dir=0
        self.move =False
        self.hp=100
        if Player.image==None:
            self.image=load_image('weapon1.png')
        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태가 Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft,
                       upkey_down: RunUp, downkey_down: RunDown, upkey_up: RunDown, downkey_up: RunUp,
                       space_down:Attact},
                RunRight: {right_up: Idle, left_down: Idle, upkey_down: RunRightUp, upkey_up: RunRightDown,
                           downkey_down: RunRightDown, downkey_up: RunRightUp},
                RunRightUp: {upkey_up: RunRight, right_up: RunUp, left_down: RunUp, downkey_down: RunRight},
                RunUp: {upkey_up: Idle, left_down: RunLeftUp, downkey_down: Idle, right_down: RunRightUp,
                        left_up: RunRightUp, right_up: RunLeftUp},
                RunLeftUp: {right_down: RunUp, downkey_down: RunLeft, left_up: RunUp, upkey_up: RunLeft},
                RunLeft: {left_up: Idle, upkey_down: RunLeftUp, right_down: Idle, downkey_down: RunLeftDown,
                          upkey_up: RunLeftDown, downkey_up: RunLeftUp},
                RunLeftDown: {left_up: RunDown, downkey_up: RunLeft, upkey_down: RunLeft, right_down: RunDown},
                RunDown: {downkey_up: Idle, left_down: RunLeftDown, upkey_down: Idle, right_down: RunRightDown,
                          left_up: RunRightDown, right_up: RunLeftDown},
                RunRightDown: {right_up: RunDown, downkey_up: RunRight, left_down: RunDown, upkey_down: RunRight},
                Attact:{attact_end:Idle,right_down: RunRight,left_down: RunLeft,upkey_down: RunUp, downkey_down: RunDown,
                        left_up: Idle, right_up: Idle,upkey_up: Idle, downkey_up: Idle},
            }
        )
        self.x,self.y=server.map.w//2,server.map.h//2
        self.font = load_font('DungGeunMo.TTF',24)

    def update(self):
        self.state_machine.update()
        if self.move:self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:self.frame=0
        self.x += math.cos(self.dir) * self.speed * game_framework.frame_time
        self.y += math.sin(self.dir) * self.speed * game_framework.frame_time

        self.x = clamp(10.0, self.x, server.map.w - 10.0)
        self.y = clamp(15.0, self.y, server.map.h - 15.0)
        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT',event))

    def draw(self):
        # self.state_machine.draw()
        sx, sy = (self.x - server.map.window_left)*4, (self.y - server.map.window_bottom)*4
        self.image.clip_draw(int(self.frame) * 64, self.action*64, 64, 64, sx, sy,100,100)
        self.font.draw(sx-35,sy+35,f'HP:{self.hp}',(255,10,10))
        draw_rectangle((self.x-server.map.window_left-5)*4,(self.y-server.map.window_bottom-10)*4,
                (self.x-server.map.window_left+5)*4,(self.y-server.map.window_bottom+5)*4)
        if self.action==0:
            draw_rectangle((self.x-server.map.window_left-7)*4,(self.y-server.map.window_bottom)*4,
                           (self.x-server.map.window_left+7)*4,(self.y-server.map.window_bottom+9)*4)
        if self.action==1:
            draw_rectangle((self.x - server.map.window_left - 9)*4, (self.y - server.map.window_bottom - 10)*4,
                           (self.x - server.map.window_left)*4, (self.y - server.map.window_bottom + 5)*4)
        if self.action==2:
            draw_rectangle((self.x - server.map.window_left)*4, (self.y - server.map.window_bottom - 10)*4,
                           (self.x - server.map.window_left + 9)*4, (self.y - server.map.window_bottom + 5)*4)
        if self.action==3:
            draw_rectangle((self.x - server.map.window_left - 7)*4, (self.y - server.map.window_bottom - 15)*4,
                            (self.x - server.map.window_left + 7)*4, (self.y - server.map.window_bottom)*4)


    def get_bb(self):
        if self.cur_state == Attact:
            pass
        return (self.x-server.map.window_left-5,self.y-server.map.window_bottom-10,
                self.x-server.map.window_left+5,self.y-server.map.window_bottom+5)
    def handle_collision(self,group,other):pass

class Idle:
    @staticmethod
    def enter(player, e):
        player.dir=0
        player.speed=0
        player.move=False
        if player.action<4:player.action+=4
        pass
    @staticmethod
    def exit(player,e):
        pass
    @staticmethod
    def do(player):
        pass

class RunRight:
    @staticmethod
    def enter(player, e):
        player.action = 6
        player.speed = RUN_SPEED_PPS
        player.dir = 0
        player.move = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass


class RunRightUp:
    @staticmethod
    def enter(player, e):
        player.action = 6
        player.speed = RUN_SPEED_PPS
        player.dir = math.pi / 4.0
        player.move = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass


class RunRightDown:
    @staticmethod
    def enter(player, e):
        player.action = 6
        player.speed = RUN_SPEED_PPS
        player.dir = -math.pi / 4.0
        player.move = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass


class RunLeft:
    @staticmethod
    def enter(player, e):
        player.action = 5
        player.speed = RUN_SPEED_PPS
        player.dir = math.pi
        player.move = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass


class RunLeftUp:
    @staticmethod
    def enter(player, e):
        player.action = 5
        player.speed = RUN_SPEED_PPS
        player.dir = math.pi * 3.0 / 4.0
        player.move = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass


class RunLeftDown:
    @staticmethod
    def enter(player, e):
        player.action = 5
        player.speed = RUN_SPEED_PPS
        player.dir = - math.pi * 3.0 / 4.0
        player.move = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass


class RunUp:
    @staticmethod
    def enter(player, e):
        player.action = 4
        player.speed = RUN_SPEED_PPS
        player.dir = math.pi / 2.0
        player.move = True

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass


class RunDown:
    @staticmethod
    def enter(player, e):
        player.action = 7
        player.speed = RUN_SPEED_PPS
        player.dir = - math.pi / 2.0
        player.move = True
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass


class Attact:
    @staticmethod
    def enter(player,e):
        player.frame = 0
        if player.action >3:player.action-=4
        player.move = True
        pass
    @staticmethod
    def exit(player,e):pass
    @staticmethod
    def do(player):
        if player.frame >3.9:
            player.move=False
            player.state_machine.add_event(('ATTACT_END',0))

    # @staticmethod
    # def draw(player):
    #     player.image.clip_draw(int(player.frame) * player.image_size_w // 4, player.action * player.image_size_h // 8,
    #                            player.image_size_w // 4, player.image_size_h // 8, player.x, player.y, 100, 100)