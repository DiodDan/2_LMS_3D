from object_3d import *
from camera import *
from projection import *
import pygame as pg
import random


chank = 3

class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        vertex, faces = self.create_map()
        vertex1, faces1 = self.create_map(step=1)
        vertex = vertex + vertex1
        faces = faces1 + faces
        vertex1, faces1 = self.create_map(step=2)
        vertex = vertex + vertex1
        faces = faces1 + faces
        vertex1, faces1 = self.create_map(step=3)
        vertex = vertex + vertex1
        faces = faces1 + faces
        self.camera = Camera(self, [1850, 450, 0])
        self.projection = Projection(self)
        self.object = Object3D(self, vertex, faces)
        """self.object.rotate_y(-math.pi / 4)"""

    """def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)"""
    def create_map(self, x=80, y=160, n=25, coef=40, step=0):
        map = []
        for i in range(n):
            for j in range(n):
                map.append((i * y, random.random() * coef, j * x + x * (n - 2) * step, 1))
        faces = []

        for i in range(1, n - 1):
            for j in range(1, n - 1):
                faces.append((i + (j - 1) * n + n * n * step, i + (j - 1) * n + 1 + n * n * step, i + j * n + 1 + n * n * step, i + j * n + n * n * step))
        return (map, faces)

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.object.draw()

    def run(self):
        global chank
        while True:
            """if self.camera.position[2] >= 1060 * chank:
                print(1)
                chank += 1
                self.object.faces = self.object.faces[842:]
                self.object.vertexes = self.object.vertexes[901:]
                vertex1, faces1 = self.create_map(step=chank + 3)
                self.object.vertex = self.object.vertex + vertex1
                self.object.faces = faces1 + self.object.faces"""

            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()