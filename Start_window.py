import random

from working.camera import *
from working.object_3d import *
from working.projection import *
from settings import *
from working.ui_items import Button
from main import start_me_up

class SoftwareRender:
    def __init__(self):
        self.plane = None
        pg.init()
        self.objects = []
        self.RES = self.WIDTH, self.HEIGHT = height - 50, width - 90
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = FPS
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()
        self.camera = Camera(self, [10, 0, -100])
        self.projection = Projection(self)
        # pg.font.init()
        self.fps_font = pg.font.SysFont('arial', 40)

    def create_objects(self):
        self.plane = Plane(self, *self.get_object_from_file('objects/Plane_low.obj'), color_mode=1)
        self.plane.rotate_y(np.pi / 2)
        self.plane.rotate_x(np.pi)
        self.plane.translate([0, 50, -300])

    def fps_show(self):
        self.screen.blit(self.fps_font.render(str(int(self.clock.get_fps())), True, (255, 255, 255)),
                         (self.WIDTH - 80, 20))

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

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.plane.rotate_y(np.pi / 360)
        self.fps_show()
        self.plane.draw()

        self.button.draw()


    def run(self):
        self.button = Button(self.screen, 150, 70, 100, 200, 1, start_me_up, "START") # surface.set_at((x, y), color)
        while True:
            self.button.update(pg.event.get())
            self.draw()
            pg.display.flip()
            self.clock.tick(self.FPS)


app = SoftwareRender()
app.run()