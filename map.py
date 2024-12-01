import server
from pico2d import*

class Map:
    def __init__(self):
        self.image = load_image('test_map.png')
        self.cw = 300#get_canvas_width()#300
        self.ch = 175#get_canvas_height()#175
        self.w = self.image.w
        self.h = self.image.h
        self.window_left=self.w//2-self.cw//2
        self.window_bottom=self.h//2-self.ch//2

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0,
                                       get_canvas_width(),get_canvas_height())
        pass

    def update(self):
        self.window_left = clamp(0, int(server.player.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.player.y) - self.ch // 2, self.h - self.ch - 1)

    def handle_event(self, event):
        pass