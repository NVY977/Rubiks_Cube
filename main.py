from ursina import *


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.fullscreen = True
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # platform
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)  # background
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model = self.model, texture = self.texture, position = pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()  # central cube
        self.rotation_axes = {'LEFT': 'x', 'RIGHT':'x', 'TOP':'y', 'BOTTOM':'y', 'FACE':'z', 'BACK':'z'}
        self.cubes_side_position = {'LEFT':self.LEFT, 'BOTTOM':self.BOTTOM, 'RIGHT': self.RIGHT, 'FACE': self.FACE,
                                    'BACK': self.BACK, 'TOP': self.TOP}
        self.animation_time = 0.5  # side rotation animation
        self.animation_tg = True  # for control animation

    def animation_trigger(self):
        self.animation_tg = not self.animation_tg

    def rotade_side(self, side_name):
        self.animation_tg = False
        cube_position = self.cubes_side_position[side_name]
        rotation_axes = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_position:
                cube.parent = self.PARENT
                #  eval - side rotation animation
                eval(f'self.PARENT.animate_rotation_{rotation_axes}(90,duration=self.animation_time)')
        invoke(self.animation_trigger, delay=self.animation_time + 0.11)

    def input(self, key):
        keys = dict(zip('asdwqe', 'LEFT BOTTOM RIGHT TOP FACE BACK'.split()))
        if key in keys and self.animation_tg:
            self.rotade_side(keys[key])
        super().input(key)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation  # remember world pos
                cube.parent = scene  # change parent
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0


    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP

if __name__ == '__main__':
    game = Game()
    game.run()
