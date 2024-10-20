from pico2d import *

# Game object class here
class Map:
    image=None
    def __init__(self):
        self.x,self.y=window_size_w//2,window_size_h//2
        self.image_size_w = 416
        self.image_size_h = 288
        self.image_x, self.image_y = self.image_size_w//2,self.image_size_h//2
        if Map.image==None:
            self.image=load_image('map.png')

    def update(self):
        pass

    def handle_event(self, event):
        if event.type==SDL_KEYDOWN and event.key==SDLK_UP:
            if self.image_y + 32 < 288-32:
                self.image_y += 5

        if event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if self.image_y - 32 >0+32:
                self.image_y -= 5

        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            if self.image_x + 96 < 416:
                self.image_x += 5

        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if self.image_x - 96 > 0:
                self.image_x -= 5
        pass

    def draw(self):
        self.image.clip_draw(self.image_x-96, self.image_y-64, 192,128, self.x, self.y,window_size_w,window_size_h)
        #self.image.draw(self.x,self.y,window_size_w,window_size_h)

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

    running = True
    world = []

    map = Map()
    world.append(map)
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
