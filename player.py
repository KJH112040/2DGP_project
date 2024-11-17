from pico2d import load_image
from state_machine import StateMachine, time_out, space_down, right_down, left_up, left_down, right_up, start_event, \
    a_down, up_keyup, down_keyup, up_keydown, down_keydown

window_size_w=1200
window_size_h=700

class Player:
    image=None
    def __init__(self):
        self.x,self.y=window_size_w//2,window_size_h//2
        self.image_size_w = 256
        self.image_size_h = 512
        self.frame=0
        self.action=7
        if Player.image==None:
            self.image=load_image('weapon1.png')
        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태가 Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: xMove, left_down: xMove,up_keydown:yMove,down_keydown:yMove, left_up: xMove, right_up: xMove,up_keyup:yMove,down_keyup: yMove},
                xMove: {right_down: Idle, left_down: Idle,up_keydown:yMove,down_keydown:yMove, right_up: Idle, left_up: Idle,up_keyup:yMove,down_keyup: yMove},
                yMove:{right_down: xMove, left_down: xMove,up_keydown:Idle,down_keydown:Idle,up_keyup:Idle,down_keyup: Idle,right_up: xMove, left_up: xMove}
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
    def enter(player, e):

        pass
    @staticmethod
    def exit(player,e):
        pass
    @staticmethod
    def do(player):
        pass
    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame*player.image_size_w//4,player.action*player.image_size_h//8, player.image_size_w//4, player.image_size_h//8, player.x, player.y, 100,100)

class xMove:
    @staticmethod
    def enter(player, e):

        pass
    @staticmethod
    def exit(player, e):
        pass
    @staticmethod
    def do(player):

        pass
    @staticmethod
    def draw(player):
        player.image.clip_draw(player.image_x - 96, player.image_y - 64, 192, 128, player.x, player.y, window_size_w, window_size_h)

class yMove:
    @staticmethod
    def enter(player,e):

        pass
    @staticmethod
    def exit(player,e):pass
    @staticmethod
    def do(player):

        pass
    @staticmethod
    def draw(player):
        player.image.clip_draw(player.image_x - 96, player.image_y - 64, 192, 128, player.x, player.y, window_size_w, window_size_h)