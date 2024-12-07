import pico2d


import game_framework
import game_world
import random
import item
import server

up_probability = [[95,5,0],[90,10,0],[85,15,0],[80,20,0],[75,25,0],
                  [70,30,0],[65,35,0],[60,40,0],[55,45,0],[50,50,0],
                  [50,47,3],[50,44,6],[50,41,9],[50,38,12],[50,35,15],
                  [50,32,18],[47,32,21],[44,32,24],[41,32,27],[38,32,30]]

class Upgrade:
    def __init__(self):
        self.image = pico2d.load_image('upgrade.png')
        self.small_font = pico2d.load_font('DungGeunMo.TTF', 12)
        self.font = pico2d.load_font('DungGeunMo.TTF', 18)
        self.big_font =pico2d.load_font('DungGeunMo.TTF', 24)
        self.select = 0
        self.select_weapon = 0
        self.success=0
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
        self.image.draw(600, 350, 1100, 600)
        self.font.draw(pico2d.get_canvas_width() // 2 - 1100 // 2 + 55, pico2d.get_canvas_height() // 2 - 20,
                       "장비:", (0, 0, 0))
        pico2d.draw_rectangle(server.bag[self.select][0].x - 30, server.bag[self.select][0].y - 30,
                              server.bag[self.select][0].x + 30, server.bag[self.select][0].y + 30)
        server.bag[self.select_weapon][0].image.draw(pico2d.get_canvas_width()//2,pico2d.get_canvas_height()//2+600//4)
        if server.bag[self.select_weapon][0].level > 0:
            self.font.draw(pico2d.get_canvas_width() // 2 + 10,
                           pico2d.get_canvas_height() // 2 + 600 // 4 - 20
                           , f'+{server.bag[self.select_weapon][0].level}', (0, 0, 0))
        if server.bag[self.select_weapon][0].level<20:
            self.font.draw(pico2d.get_canvas_width() // 2 - 1100 // 2 + 55,pico2d.get_canvas_height()//2+600//4+20,
                        f'성공 확률:{up_probability[server.bag[self.select_weapon][0].level][0]}',(0,0,0))
            self.font.draw(pico2d.get_canvas_width() // 2 - 1100 // 2 + 55, pico2d.get_canvas_height() // 2 + 600 // 4,
                        f'실패 확률:{up_probability[server.bag[self.select_weapon][0].level][1]}', (0, 0, 0))
            self.font.draw(pico2d.get_canvas_width() // 2 - 1100 // 2 + 55, pico2d.get_canvas_height() // 2 + 600 // 4-20,
                        f'하락 확률:{up_probability[server.bag[self.select_weapon][0].level][2]}', (0, 0, 0))
        else:
            self.big_font.draw(pico2d.get_canvas_width() // 2 - 1100 // 2 + 55, pico2d.get_canvas_height() // 2 + 600 // 4,
                        f'최대 레벨', (0, 0, 0))
        if self.success==1:
            self.big_font.draw(pico2d.get_canvas_width() // 2-55,
                               pico2d.get_canvas_height() // 2 + 600 // 2 - 70,
                               f'강화 성공!!', (0, 255, 255))
        elif self.success==2:
            self.big_font.draw(pico2d.get_canvas_width() // 2-55,
                               pico2d.get_canvas_height() // 2 + 600 // 2 - 70,
                               f'강화 실패', (0, 0, 0))
        elif self.success==3:
            self.big_font.draw(pico2d.get_canvas_width() // 2-55,
                               pico2d.get_canvas_height() // 2 + 600 // 2 - 70,
                               f'레벨 하락...', (255, 0, 0))
        for i in range(len(server.bag)//2):
            if type(server.bag[i][0]) == item.Weapon:
                server.bag[i][0].draw()
                if server.bag[i][0].level > 0:
                    self.font.draw(server.bag[i][0].x + 10, server.bag[i][0].y - 20, f'+{server.bag[i][0].level}',(0,0,0))
                if server.bag[i][0].set == True:
                    self.font.draw(server.bag[i][0].x - 30, server.bag[i][0].y + 20, f'장착 중', (255, 255, 100))
        self.small_font.draw(server.bag[self.select_weapon][0].x - 20, server.bag[self.select_weapon][0].y,
                       '강화 중', (255, 0, 0))

    def update(self):pass

def init():
    global upgrade
    upgrade = Upgrade()
    game_world.add_object(upgrade,2)

def finish():
    global upgrade
    game_world.remove_object(upgrade)

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
                    if upgrade.select != 0:
                        if type(server.bag[upgrade.select - 1][0]) == item.Weapon:
                            upgrade.select -= 1
                case pico2d.SDLK_RIGHT:
                    if upgrade.select != 19:
                        if type(server.bag[upgrade.select + 1][0]) == item.Weapon:
                            upgrade.select += 1
                case pico2d.SDLK_RETURN:
                    if type(server.bag[upgrade.select][0]) == item.Weapon:
                        upgrade.select_weapon = upgrade.select
                        upgrade.success=0
                case pico2d.SDLK_SPACE:
                    if server.bag[upgrade.select_weapon][0].level<20:
                        up=random.randint(1,100)
                        if up<=up_probability[server.bag[upgrade.select_weapon][0].level][0]:
                            server.bag[upgrade.select_weapon][0].level += 1
                            server.bag[upgrade.select_weapon][0].attack += 5
                            upgrade.success = 1
                        elif up >up_probability[server.bag[upgrade.select_weapon][0].level][0]+up_probability[server.bag[upgrade.select_weapon][0].level][1]:
                            server.bag[upgrade.select_weapon][0].level -= 1
                            server.bag[upgrade.select_weapon][0].attack -= 5
                            upgrade.success = 3
                        else:upgrade.success=2



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