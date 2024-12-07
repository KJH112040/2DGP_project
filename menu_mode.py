import pico2d

import game_framework
import game_world
import equip_mode
import bag_mode
import upgrade_mode

class Menu:
    def __init__(self):
        self.image = pico2d.load_image('menu_window-Sheet.png')

    def draw(self):
        global select_menu
        self.image.draw(600,350)
        match select_menu:
            case 0:
                pico2d.draw_rectangle(pico2d.get_canvas_width()//2-192//2,pico2d.get_canvas_height()//2+256//4,
                                      pico2d.get_canvas_width()//2+192//2,pico2d.get_canvas_height()//2+256//2)
            case 1:
                pico2d.draw_rectangle(pico2d.get_canvas_width()//2-192//2,pico2d.get_canvas_height()//2,
                                      pico2d.get_canvas_width()//2+192//2,pico2d.get_canvas_height()//2+256//4)
            case 2:
                pico2d.draw_rectangle(pico2d.get_canvas_width() // 2 - 192 // 2, pico2d.get_canvas_height() // 2 - 256 // 4,
                                     pico2d.get_canvas_width() // 2 + 192 // 2, pico2d.get_canvas_height() // 2)
            case 3:
                pico2d.draw_rectangle(pico2d.get_canvas_width() // 2 - 192 // 2, pico2d.get_canvas_height() // 2 - 256 // 2,
                                      pico2d.get_canvas_width() // 2 + 192 // 2, pico2d.get_canvas_height() // 2 - 256 // 4)


    def update(self):
        pass

def init():
    global menu, select_menu
    menu = Menu()
    game_world.add_object(menu,2)
    select_menu=0

def finish():
    game_world.remove_object(menu)

def handle_events():
    global select_menu
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
                case pico2d.SDLK_UP:
                    select_menu -= 1
                    if select_menu < 0:
                        select_menu = 3
                case pico2d.SDLK_DOWN:
                    select_menu += 1
                    if select_menu > 3:
                        select_menu = 0
                case pico2d.SDLK_RETURN:
                    match select_menu:
                        case 0:
                            game_framework.push_mode(equip_mode)
                        case 1:
                            game_framework.push_mode(bag_mode)
                        case 2:
                            game_framework.push_mode(upgrade_mode)
                        case 3:
                            game_framework.quit()

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