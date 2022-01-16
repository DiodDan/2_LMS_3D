from working.camera import *
from working.object_3d import *
from working.projection import *
from settings import *
from working.ui_items import Button

class score_window:
    def __init__(self, start_me_up):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = height - 50, width - 90
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = FPS
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.camera = Camera(self, [10, 0, -100])
        self.projection = Projection(self)
        self.fps_font = pg.font.SysFont('arial', 40)
        self.profile = 'None'
        self.score = 0
        """self.menu_button = Button(self.screen, 100, 50, 500, 500, 1, 
        Start_window.SoftwareRender().run("profile", 999), "Menu")"""
        self.replay_button = Button(self.screen, 200, 70, 500, 570, 1,
                                    lambda: start_me_up(self.profile),
                                    "replay")

    def fps_show(self):
        self.screen.blit(
            self.fps_font.render(str(int(self.clock.get_fps())), True,
                                 (255, 255, 255)),
            (self.WIDTH - 80, 20))

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.replay_button.update(pg.event.get())
        self.replay_button.draw()
        self.fps_show()
        self.screen.blit(
            self.fps_font.render(
                'profile: ' + str(self.profile) + "\n" + "score: " + str(
                    self.score), True,
                (255, 255, 255)), (10, 20))

    def run(self, prof='None', score=0):
        self.profile = prof
        self.score = score

        while True:
            self.draw()
            pg.display.flip()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(self.FPS)


def end_game(profile, score, start):
    app = score_window(start)
    app.run(profile, score)
