from pico2d import load_image
from state_machine import StateMachine, time_out, space_down, right_down, left_up, left_down, right_up, start_event, \
    a_down, up_keyup, down_keyup, up_keydown, down_keydown

window_size_w=1200
window_size_h=700

class Map:
    image=None
    def __init__(self):
        self.x,self.y=window_size_w//2,window_size_h//2
        self.image_size_w = 416
        self.image_size_h = 288
        self.dir_x=0
        self.dir_y=0
        self.image_x, self.image_y = self.image_size_w//2,self.image_size_h//2
        if Map.image==None:
            self.image=load_image('test_map.png')
        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태가 Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: xMove, left_down: xMove, up_keydown: yMove, down_keydown: yMove, left_up: xMove,
                       right_up: xMove, up_keyup: yMove, down_keyup: yMove},
                xMove: {right_down: Idle, left_down: Idle, up_keydown: yMove, down_keydown: yMove, right_up: Idle,
                        left_up: Idle, up_keyup: xMove, down_keyup: xMove},
                yMove: {right_down: xMove, left_down: xMove, up_keydown: Idle, down_keydown: Idle, up_keyup: Idle,
                        down_keyup: Idle, right_up: yMove, left_up: yMove}
                # 나중에 캐릭터 움직임 구현하면 캐릭터 움직임 이벤트와 같이 처리되도록 수정할 부분!
                # 캐릭터 사망 시 이벤트로 시작했던 위치로 되돌아 가도록!
            }
        )

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT',event))

    def draw(self):
        self.state_machine.draw()

class Idle:
    @staticmethod
    def enter(map, e):
        map.dir_x = 0
        map.dir_y = 0
        pass
    @staticmethod
    def exit(map,e):
        pass
    @staticmethod
    def do(map):
        pass
    @staticmethod
    def draw(map):
        map.image.clip_draw(map.image_x - 96, map.image_y - 64, 192, 128, map.x, map.y, window_size_w,window_size_h)

class xMove:
    @staticmethod
    def enter(map, e):
        if up_keyup(e) or down_keyup(e)or up_keydown(e) or down_keydown(e)or right_up(e)or left_up(e):
            map.dir_x=0
        elif right_down(e) :
            map.dir_x = 1
        elif left_down(e) :
            map.dir_x = -1
        pass
    @staticmethod
    def exit(map, e):
        pass
    @staticmethod
    def do(map):
        if map.dir_x==1 and map.image_x + 96 < map.image_size_w:
            map.image_x += map.dir_x * 4
        elif map.dir_x==-1 and map.image_x -96 > 0:
            map.image_x += map.dir_x * 4
        pass
    @staticmethod
    def draw(map):
        map.image.clip_draw(map.image_x - 96, map.image_y - 64, 192, 128, map.x, map.y, window_size_w, window_size_h)

class yMove:
    @staticmethod
    def enter(map,e):
        if right_up(e) or left_up(e) or right_down(e) or left_down(e) or up_keyup(e) or down_keyup(e):
            map.dir_y =0
        elif up_keydown(e) :
            map.dir_y = 1
        elif down_keydown(e):
            map.dir_y = -1
        pass
    @staticmethod
    def exit(map,e):pass
    @staticmethod
    def do(map):
        if map.dir_y==1 and map.image_y +64 <map.image_size_h:
            map.image_y += map.dir_y * 4
        elif map.dir_y==-1 and map.image_y - 64 >0:
            map.image_y += map.dir_y * 4
        pass
    @staticmethod
    def draw(map):
        map.image.clip_draw(map.image_x - 96, map.image_y - 64, 192, 128, map.x, map.y, window_size_w, window_size_h)