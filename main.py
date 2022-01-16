import random
import sqlite3
from working.camera import *
from working.object_3d import *
from working.projection import *
from settings import *
import score_window


class SoftwareRender:
    def __init__(self):
        self.plane = None
        pg.init()
        self.objects = []
        self.coins = []
        self.walls = []
        self.RES = self.WIDTH, self.HEIGHT = height - 50, width - 90
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = FPS
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects(chunk, chunk_size)
        self.camera = Camera(self, camera_start_position)
        self.projection = Projection(self)
        self.fps_font = pg.font.SysFont('arial', 40)
        self.count = 0
        self.score = 0
        self.profile = None

    def create_objects(self, _chunk, _chunk_size):
        self.plane = Plane(self, *self.get_object_from_file(
            'objects/Plane_low.obj'), color_mode=2)
        for i in range(in_time_chunks):
            self.objects.append(Object3D(self, *self.create_map(x=chunk_size_x,
                                                                y=chunk_size_y,
                                                                n=chunk_rect_n,
                                                                ratio=z_scale,
                                                                step=i)))
        for i in range(8):
            self.coins.append(Coin(self, *self.get_object_from_file(
                'objects/Coin.obj'), color_mode=3))
            self.coins[-1].translate([random.randint(1000, 4000), 450,
                                      _chunk_size * (
                                    _chunk + i // 4) - _chunk_size // 5 * (
                                                  i % 4 + 1)])
            self.walls.append(
                Coin(self, *self.get_object_from_file('objects/wall.obj'),
                     color_mode=4))
            self.walls[-1].translate([random.choice(list(range(0, 4000))[
                                                    1000:int(
                                                        self.coins[-1].point[
                                                            0]) - 800] + list(
                range(0, 4000))[int(self.coins[-1].point[0]) + 800:4000]), 450,
                                      _chunk_size * (
                                _chunk + i // 4) - _chunk_size // 5 * (
                                              i % 4 + 1)])

        self.plane.rotate_y(np.pi / 2)
        self.plane.translate(plane_start_position)

    def fps_show(self):
        self.screen.blit(
            self.fps_font.render(str(int(self.clock.get_fps())), True,
                                 (255, 255, 255)),
            (self.WIDTH - 60, 20))

    def score_show(self):
        self.screen.blit(
            self.fps_font.render(('Score: ' + str(self.score)), True,
                                 (0, 204, 255)), (20, 20))

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
        global plane_moving_speed
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
        for i in range(len(self.coins)):
            self.coins[i].rotate_y(np.pi / 400)
            self.coins[i].draw()
            self.walls[i].rotate_y(np.pi / 400)
            self.walls[i].draw()

        self.fps_show()
        self.score_show()
        self.plane.draw()

    def collision_check(self):
        for i in range(len(self.coins)):
            money_rect = pg.Rect(self.coins[i].point[0] - 50,
                                 self.coins[i].point[2] - 50, 100, 100)
            wall_rect = pg.Rect(self.walls[i].point[0] - 300,
                                self.walls[i].point[2] - 300, 600, 600)
            plane_rect = pg.Rect(abs(self.plane.vertexes[0][0]) - 50,
                                 abs(self.plane.vertexes[0][2]) + 150, 180,
                                 100)
            if pg.Rect.colliderect(money_rect, plane_rect):
                self.coins[i].translate([-1000, 0, -1000])
                self.score += 10
                break
            if pg.Rect.colliderect(wall_rect, plane_rect):
                con = sqlite3.connect("players.db")
                cur = con.cursor()
                result = cur.execute("""SELECT * FROM data""").fetchall()
                for elem in result:
                    if self.profile == elem[0]:
                        max_score = int(elem[1])
                        if int(self.score) > max_score:
                            cur.execute(
                                f"""UPDATE data SET score={self.score}
                                 WHERE name='{self.profile}'""")
                            con.commit()
                        break

                con.close()
                score_window.end_game(self.profile, self.score, start_me_up)
                break

    def spawn_objects(self, _chunk, _chunk_size):
        for i in range(4):
            self.coins.append(
                Coin(self, *self.get_object_from_file('objects/Coin.obj'),
                     color_mode=3))
            self.coins[-1].translate([random.randint(1000, 4000), 450,
                                      _chunk_size * (
                                                  _chunk + 1) - _chunk_size // 5 * (
                                                  i % 4 + 1)])
            self.walls.append(
                Coin(self, *self.get_object_from_file('objects/wall.obj'),
                     color_mode=4))
            self.walls[-1].translate([random.choice(list(range(0, 4000))[
                                                    1000:int(
                                                        self.coins[-1].point[
                                                            0]) - 800] + list(
                range(0, 4000))[int(self.coins[-1].point[0]) + 800:4000]), 450,
                                      _chunk_size * (
                                                  _chunk + 1) - _chunk_size // 5 * (
                                                  i % 4 + 1)])

    def run(self, _chunk, _chunk_size):
        global plane_moving_speed
        while True:
            if self.camera.position[2] >= _chunk * _chunk_size:
                del self.objects[0]
                del self.coins[:4]
                del self.walls[:4]
                self.objects.append(Object3D(self,
                                             *self.create_map(x=chunk_size_x,
                                                              y=chunk_size_y,
                                                              n=chunk_rect_n,
                                                              ratio=z_scale,
                                                              step=_chunk + in_time_chunks - 1)))
                _chunk += 1
                self.spawn_objects(_chunk, _chunk_size)
                self.objects[-1].dir = bool(self.objects[-2].dir)
                self.objects[-1].color = self.objects[-2].color.copy()
            self.collision_check()
            self.draw()
            self.camera.control(10 + self.score * 0.1)
            plane_moving_speed = 10 + self.score * 0.1
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(self.FPS)


def start_me_up(profile):
    app = SoftwareRender()
    app.profile = profile
    app.run(chunk, chunk_size)
