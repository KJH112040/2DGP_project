import server

objects = [[] for _ in range(4)]
collision_pairs={}

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()
    collision_pairs.clear()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def attack_collide(a, b):
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if a[0] > right_b: return False
    if a[2] < left_b: return False
    if a[3] < bottom_b: return False
    if a[1] > top_b: return False

    return True


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

                if group == 'attack:monster':
                    if a.action==0:
                        a_bb = [a.x-server.map.window_left-7,a.y-server.map.window_bottom,
                                a.x-server.map.window_left+7,a.y-server.map.window_bottom+9]
                    elif a.action==1:
                        a_bb = [a.x - server.map.window_left - 9, a.y - server.map.window_bottom - 10,
                                a.x - server.map.window_left, a.y - server.map.window_bottom + 5]
                    elif a.action==2:
                        a_bb = [a.x - server.map.window_left, a.y - server.map.window_bottom - 10,
                                a.x - server.map.window_left + 9, a.y - server.map.window_bottom + 5]
                    elif a.action==3:
                        a_bb = [a.x - server.map.window_left - 7, a.y - server.map.window_bottom - 15,
                                a.x - server.map.window_left + 7, a.y - server.map.window_bottom]

                    if attack_collide(a_bb,b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)

