import pico2d

import game_framework
import game_world
import item
import server

class Equip:
    def __init__(self):
        self.image = pico2d.load_image('equip.png')
        self.font = pico2d.load_font('DungGeunMo.TTF', 18)
        self.select = 0
        item_x = pico2d.get_canvas_width() // 2 - 1100 // 2 + 90
        item_y = pico2d.get_canvas_height() // 2 - 70
        for i in range(len(server.bag) // 2):
            if type(server.bag[i][0]) == item.Weapon:
                server.bag[i][0].x = item_x
                server.bag[i][0].y = item_y
                if item_x < pico2d.get_canvas_width() // 2 + 1100 // 2 - 90:
                    item_x += 70
                else:
                    item_x = pico2d.get_canvas_width() // 2 - 1100 // 2 + 90
                    item_y -= 70

    def draw(self):
        self.image.draw(600,350,1100,600)
        self.font.draw(pico2d.get_canvas_width()//2-1100//2+55,pico2d.get_canvas_height()//2+600//2-50,
                       "현재 장착 중인 장비:",(0,0,0))
        self.font.draw(pico2d.get_canvas_width() // 2 + 25, pico2d.get_canvas_height() // 2 + 600 // 2 - 50,
                       "장비 장착 효과:", (0, 0, 0))
        self.font.draw(pico2d.get_canvas_width() // 2 - 1100 // 2 + 55, pico2d.get_canvas_height() // 2 - 20,
                       "장비:", (0, 0, 0))
        pico2d.draw_rectangle(server.bag[self.select][0].x - 30, server.bag[self.select][0].y - 30,
                              server.bag[self.select][0].x + 30, server.bag[self.select][0].y + 30)
        for i in range(len(server.bag)//2):
            if type(server.bag[i][0]) == item.Weapon:
                server.bag[i][0].draw()
                if server.bag[i][0].level > 0:
                    self.font.draw(server.bag[i][0].x + 10, server.bag[i][0].y - 20, f'+{server.bag[i][0].level}',(0,0,0))
                if server.bag[i][0].set == True:
                    server.bag[i][0].image.draw(pico2d.get_canvas_width()//2-1100//2+90,
                                                pico2d.get_canvas_height()//2+600//2-90)
                    if server.bag[i][0].weapon_id == 1:
                        self.font.draw(pico2d.get_canvas_width()//2-1100//2+70,
                                       pico2d.get_canvas_height()//2+600//2-160,
                                       '평범한 나무 몽둥이',(0,0,0))
                    self.font.draw(pico2d.get_canvas_width() // 2 + 40, pico2d.get_canvas_height() // 2 + 600 // 2 - 80,
                                   f'공격력 : {server.bag[i][0].attack}')
                    if server.bag[i][0].level > 0:
                        self.font.draw(pico2d.get_canvas_width()//2-1100//2+100,
                                        pico2d.get_canvas_height()//2+600//2-110
                                       , f'+{server.bag[i][0].level}',(0, 0, 0))
                    self.font.draw(server.bag[i][0].x - 30, server.bag[i][0].y + 20, f'장착 중',(255, 255, 100))

    def update(self):
        pass


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
                case pico2d.SDLK_LEFT:
                    if equip.select != 0:
                        if type(server.bag[equip.select - 1][0]) == item.Weapon:
                            equip.select -= 1
                case pico2d.SDLK_RIGHT:
                    if equip.select != 19:
                        if type(server.bag[equip.select + 1][0]) == item.Weapon:
                            equip.select += 1
                case pico2d.SDLK_RETURN:
                    if type(server.bag[equip.select][0]) == item.Weapon:
                        if server.bag[equip.select][0].set != True:
                            for i in range(len(server.bag) // 2):
                                if type(server.bag[i][0]) == item.Weapon:
                                    if server.bag[i][0].set == True:
                                        server.bag[i][0].set=False
                                        break
                            server.bag[equip.select][0].set=True


def update():
    pass

def draw():
    pico2d.clear_canvas()
    game_world.render()
    pico2d.update_canvas()

def pause():
    pass

def resume():
    pass