from pico2d import load_image

class Weapon:
    def __init__(self, id):
        self.weapon_id = id  # 1 = 나무 막대기
        self.level = 0
        self.attact = 5 # 공격력
        match self.weapon_id:
            case 1:
                self.image = load_image('wooden_stick.png')

class Potion:
    def __init__(self, id):
        pass
