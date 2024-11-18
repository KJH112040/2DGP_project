from pico2d import *
import game_framework

import game_world
from map import Map
from player import Player

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            map.handle_event(event)
            player.handle_event(event)

def init():
    global map
    global player

    map = Map()
    game_world.add_object(map, 0)

    player = Player()
    game_world.add_object(player, 1)


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

