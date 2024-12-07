from pico2d import load_image

class Weapon:
    def __init__(self, id):
        self.weapon_id = id  # 1 = 나무 막대기
        self.level = 0
        self.attack = 5 # 공격력
        self.set = False
        match self.weapon_id:
            case 1:
                self.image = load_image('wooden_stick.png')
        self.x,self.y =0,0

    def draw(self):
        self.image.draw(self.x,self.y)
    def update(self):pass

class Potion:
    def __init__(self, id):
        self.x,self.y =0,0
        pass

    def draw(self):pass
    def update(self):pass