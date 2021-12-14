import random

from working.camera import *
from working.object_3d import *
from working.projection import *
from settings import *


class SoftwareRender:
    def __init__(self):
        self.plane = None
        pg.init()
        self.objects = []
        self.coins = []
        self.RES = self.WIDTH, self.HEIGHT = height, width
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = FPS
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()
        self.camera = Camera(self, camera_start_position)
        self.projection = Projection(self)

    def create_objects(self):
        self.plane = Plane(self, *self.get_object_from_file("objects/Plane.obj"),
                           color_mode=2)
        for i in range(in_time_chunks):
            self.objects.append(Object3D(self, *self.create_map(x=chunk_size_x,
                                                                y=chunk_size_y,
                                                                n=chunk_rect_n,
                                                                ratio=z_scale,
                                                                step=i)))

        self.coins.append(
            Coin(self, *self.get_object_from_file("objects/Coin.obj"), color_mode=3))
        self.coins[-1].translate([2875, 450, 2000])
        self.plane.rotate_y(np.pi / 2)
        self.plane.translate(plane_start_position)

    @staticmethod
    def get_object_from_file(filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append(
                        [int(face_.split('/')[0]) - 1 for face_ in faces_])
        return vertex, faces

    @staticmethod
    def create_map(x, y, n, ratio, step):
        map_matrix = []
        for i in range(n):
            for j in range(n):
                map_matrix.append((i * y, random.random() * ratio,
                                   j * x + x * (n - 1) * step, 1))
        faces = []
        for i in range(0, n - 1):
            for j in range(0, n - 1):
                faces.append((i + j * n, i + j * n + 1,
                              i + (j + 1) * n + 1, i + (j + 1) * n))
        return map_matrix, faces

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.plane.translate([0, 0, plane_moving_speed])
        if self.plane.real_angle > 0:
            self.plane.rotate_z(np.pi / (flip_speed * flip_return_ratio))
            self.plane.real_angle -= np.pi / (flip_speed * flip_return_ratio)
        if self.plane.real_angle < 0:
            self.plane.rotate_z(-np.pi / (flip_speed * flip_return_ratio))
            self.plane.real_angle -= -np.pi / (flip_speed * flip_return_ratio)
        for obj in self.objects:
            obj.draw()
        for coin in self.coins:
            coin.rotate_y(np.pi / 400)
            coin.draw()
        self.plane.draw()

    def run(self, _chunk, _chunk_size):
        while True:
            if self.camera.position[2] >= _chunk * _chunk_size:
                del self.objects[0]
                self.objects.append(Object3D(self,
                                             *self.create_map(x=chunk_size_x,
                                                              y=chunk_size_y,
                                                              n=chunk_rect_n,
                                                              ratio=z_scale,
                                                              step=_chunk + in_time_chunks - 1)))
                self.objects[-1].dir = bool(self.objects[-2].dir)
                self.objects[-1].color = self.objects[-2].color.copy()
                _chunk += 1
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = SoftwareRender()
    app.run(chunk, chunk_size)
