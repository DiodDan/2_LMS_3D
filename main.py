import objects as objects

from object_3d import *
from camera import *
from projection import *
import pygame as pg
import random


chank = 1
chank_size = 0
in_time_chunks = 4
class SoftwareRender:
    def __init__(self):
        pg.init()
        self.objects = []
        self.plane = ''
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()


    def create_objects(self):
        self.camera = Camera(self, [2875, 600, 0])
        self.projection = Projection(self)
        for i in range(in_time_chunks):
            self.objects.append(Object3D(self, *self.create_map(step=i)))
        self.plane = Plane(self, *self.get_object_from_file("plane v1.obj"), color_mode=2)
        self.plane.rotate_x(np.pi / 2)
        self.plane.rotate_z(np.pi / 2)
        self.plane.translate([2863, 450, 350])

        """self.object.rotate_y(-math.pi / 4)"""

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return vertex, faces
    def create_map(self, x=450, y=250, n=26, coef=40, step=0):
        map = []
        global chank_size
        chank_size = (n - 2) * x
        for i in range(n):
            for j in range(n):
                map.append((i * y, random.random() * coef, j * x + x * (n - 2) * step, 1))
        faces = []

        for i in range(1, n - 1):
            for j in range(1, n - 1):
                faces.append((i + (j - 1) * n, i + (j - 1) * n + 1, i + j * n + 1, i + j * n))
        return map, faces

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.plane.translate([0, 0, 10])
        if self.plane.real_angle > 0:
            self.plane.rotate_z(np.pi / 400)
            self.plane.real_angle -= np.pi / 400
        if self.plane.real_angle < 0:
            self.plane.rotate_z(-np.pi / 400)
            self.plane.real_angle -= -np.pi / 400
        for obj in self.objects:
            obj.draw()
        self.plane.draw()
    def run(self):
        global chank
        while True:
            if self.camera.position[2] >= chank * chank_size:
                del self.objects[0]
                self.objects.append(Object3D(self, *self.create_map(step=chank + in_time_chunks - 1)))
                self.objects[-1].dir = bool(self.objects[-2].dir)
                self.objects[-1].color = self.objects[-2].color.copy()
                chank += 1
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()