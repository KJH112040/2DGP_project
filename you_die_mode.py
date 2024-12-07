
import game_framework
import pico2d
import game_world
import server

class Youdie:
    def __init__(self):
        self.font = pico2d.load_font('DungGeunMo.ttf', 60)
        self.font_sub =pico2d.load_font('DungGeunMo.ttf', 24)

    def update(self):pass

    def draw(self):
        die.font.draw(pico2d.get_canvas_width() // 2 - 310, pico2d.get_canvas_height() // 2 + 150,
                      '당신은 사망하셨습니다.', (255, 0, 0))
        die.font.draw(pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 2,
                      f'{int(10 - (pico2d.get_time() - youdie_start_time))}', (0, 255, 255))
        die.font_sub.draw(pico2d.get_canvas_width() // 2 - 150, pico2d.get_canvas_height() // 4,
                        '바로 부활',(0,0,0))
        die.font_sub.draw(pico2d.get_canvas_width() // 2 + 80, pico2d.get_canvas_height() // 4,
                          '종료', (0, 0, 0))

        global select
        if select==0:
            pico2d.draw_rectangle(pico2d.get_canvas_width() // 2 - 200, pico2d.get_canvas_height() // 4 - 25,
                                  pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 4 + 25)
        else:
            pico2d.draw_rectangle(pico2d.get_canvas_width() // 2, pico2d.get_canvas_height() // 4 - 25,
                                  pico2d.get_canvas_width() // 2 + 200, pico2d.get_canvas_height() // 4 + 25)

def init():
    global youdie_start_time, die, select

    die = Youdie()
    game_world.add_object(die,2)
    select=0
    youdie_start_time = pico2d.get_time()

def finish():
    global die
    game_world.remove_object(die)
    server.player.x,server.player.y =server.map.w//2,server.map.h//2
    server.player.frame = 0
    server.player.action = 7
    server.player.dir = 0
    server.player.move = False
    server.player.hp = 100
    server.player.inv = 0
    server.player.col_attack = False


def update():
    global youdie_start_time
    if pico2d.get_time()- youdie_start_time>= 10.0:
        youdie_start_time = pico2d.get_time()
        game_framework.pop_mode()

def draw():
    pico2d.clear_canvas()
    game_world.render()
    pico2d.update_canvas()

def handle_events():
    global select
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_LEFT:
                    if select==0: select=1
                    else: select=0
                case pico2d.SDLK_RIGHT:
                    if select == 0:
                        select = 1
                    else:
                        select = 0
                case pico2d.SDLK_RETURN:
                    if select==0:game_framework.pop_mode()
                    else: game_framework.quit()