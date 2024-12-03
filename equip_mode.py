import pico2d

import game_framework
import game_world

class Equip:
    def __init__(self):
        self.image = pico2d.load_image('equip.png')
        self.font = pico2d.load_font('DungGeunMo.TTF', 18)

    def draw(self):
        self.image.draw(600,350,1100,600)
        self.font.draw(pico2d.get_canvas_width()//2-1100//2+55,pico2d.get_canvas_height()//2+600//2-50,
                       "현재 장착 중인 장비:",(0,0,0))
        self.font.draw(pico2d.get_canvas_width() // 2 + 25, pico2d.get_canvas_height() // 2 + 600 // 2 - 50,
                       "장비 장착 효과:", (0, 0, 0))
        self.font.draw(pico2d.get_canvas_width() // 2 - 1100 // 2 + 55, pico2d.get_canvas_height() // 2 - 20,
                       "장비:", (0, 0, 0))


def init():
    global equip
    equip = Equip()
    game_world.add_object(equip,2)

def finish():
    global equip
    game_world.remove_object(equip)

def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()


def update():
    pass

def draw():
    pico2d.clear_canvas()
    #pannel.image.draw(400,300)
    game_world.render()
    pico2d.update_canvas()

def pause():
    pass

def resume():
    pass