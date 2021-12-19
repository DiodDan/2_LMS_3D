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
        self.RES = self.WIDTH, self.HEIGHT = height - 50, width - 90
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = FPS
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects(chunk, chunk_size)
        self.camera = Camera(self, camera_start_position)
        self.projection = Projection(self)
        # pg.font.init()
        self.fps_font = pg.font.SysFont('arial', 40)
        self.count = 0
        self.last = -1
        self.score = 0

    def create_start_money(self, _chunk, _chunk_size):
        for i in range(8):
            self.coins.append(
                Coin(self, *self.get_object_from_file('objects/Coin.obj'), color_mode=3))
        x1, x2, x3, x4, x5, x6, x7, x8 = [random.randint(1000, 4000) for i in range(8)]
        self.coins[0].translate([x1, 450, _chunk_size * _chunk - _chunk_size // 5])
        self.coins[1].translate([x2, 450, _chunk_size * _chunk - _chunk_size // 5 * 2])
        self.coins[2].translate([x3, 450, _chunk_size * _chunk - _chunk_size // 5 * 3])
        self.coins[3].translate([x4, 450, _chunk_size * _chunk - _chunk_size // 5 * 4])
        self.coins[4].translate([x5, 450, _chunk_size * (_chunk + 1) - _chunk_size // 5])
        self.coins[5].translate([x6, 450, _chunk_size * (_chunk + 1) - _chunk_size // 5 * 2])
        self.coins[6].translate([x7, 450, _chunk_size * (_chunk + 1) - _chunk_size // 5 * 3])
        self.coins[7].translate([x8, 450, _chunk_size * (_chunk + 1) - _chunk_size // 5 * 4])

    def create_objects(self, _chunk, _chunk_size):
        self.plane = Plane(self, *self.get_object_from_file('objects/Plane_low.obj'), color_mode=2)
        for i in range(in_time_chunks):
            self.objects.append(Object3D(self, *self.create_map(x=chunk_size_x,
                                                                y=chunk_size_y,
                                                                n=chunk_rect_n,
                                                                ratio=z_scale,
                                                                step=i)))
        self.create_start_money(_chunk, _chunk_size)
        self.plane.rotate_y(np.pi / 2)
        self.plane.translate(plane_start_position)

    def fps_show(self):
        self.screen.blit(self.fps_font.render(str(int(self.clock.get_fps())), True, (255, 255, 255)),
                         (self.WIDTH - 60, 20))

    def score_show(self):
        self.screen.blit(self.fps_font.render(('Score: ' + str(self.score)), True, (0, 204, 255)), (20, 20))

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
    @njit
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
        self.fps_show()
        self.score_show()
        self.plane.draw()

    def exammoney(self):
        for i in range(len(self.coins)):
            money_rect = pg.Rect(abs(self.coins[i].vertexes[0][0]), abs(self.coins[i].vertexes[0][2]), 100, 100)
            plane_rect = pg.Rect(abs(self.plane.vertexes[0][0]) - 50, abs(self.plane.vertexes[0][2]) + 150, 180, 100)
            if pg.Rect.colliderect(money_rect, plane_rect):
                if i != self.last:
                    self.coins[i].translate([-1000, 0, -1000])
                    self.last = i
                    self.score += 10
                    print(self.score)
                    break

    def money_spavn(self, _chunk, _chunk_size):
        for i in range(4):
            self.coins.append(
                Coin(self, *self.get_object_from_file('objects/Coin.obj'), color_mode=3))
        x1, x2, x3, x4 = [random.randint(1000, 4000) for i in range(4)]
        self.coins[4].translate([x1, 450, _chunk_size * (_chunk + 1) - _chunk_size // 5])
        self.coins[5].translate([x2, 450, _chunk_size * (_chunk + 1) - _chunk_size // 5 * 2])
        self.coins[6].translate([x3, 450, _chunk_size * (_chunk + 1) - _chunk_size // 5 * 3])
        self.coins[7].translate([x4, 450, _chunk_size * (_chunk + 1) - _chunk_size // 5 * 4])

    def run(self, _chunk, _chunk_size):
        while True:
            if self.camera.position[2] >= _chunk * _chunk_size:
                del self.objects[0]
                del self.coins[:4]
                self.objects.append(Object3D(self,
                                             *self.create_map(x=chunk_size_x,
                                                              y=chunk_size_y,
                                                              n=chunk_rect_n,
                                                              ratio=z_scale,
                                                              step=_chunk + in_time_chunks - 1)))
                _chunk += 1
                self.money_spavn(_chunk, _chunk_size)
                self.objects[-1].dir = bool(self.objects[-2].dir)
                self.objects[-1].color = self.objects[-2].color.copy()
            self.exammoney()
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(self.FPS)


def start_me_up():
    app = SoftwareRender()
    app.run(chunk, chunk_size)
