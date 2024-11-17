from pico2d import *

import player as Player
import map as Map

# Game object class here
def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            map.handle_event(event)
            pass

def reset_world():
    global running
    global world
    global map
    global player

    running = True
    world = []

    map = Map.Map()
    world.append(map)
    player=Player.Player()
    world.append(player)
    pass


def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

window_size_w=1200
window_size_h=700

open_canvas(window_size_w,window_size_h)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
