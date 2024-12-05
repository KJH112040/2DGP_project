from pico2d import *
import game_framework
import game_world
import server
from player import Player
from map import Map
from item import Weapon
from monster import Monster
import menu_mode

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_m:
            game_framework.push_mode(menu_mode)
        else:
            server.player.handle_event(event)

def init():
    server.map = Map()
    game_world.add_object(server.map, 0)

    server.player = Player()
    game_world.add_object(server.player, 1)

    for i in range(50):
        monster = Monster()
        game_world.add_object(monster,1)

    for i in range(5):
        server.bag[i][0]=Weapon(1)
        server.bag[i][1]=1


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    #delay(0.01)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

