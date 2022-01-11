import random
import sqlite3
from working.camera import *
from working.object_3d import *
from working.projection import *
from settings import *
from working.ui_items import Button, Textline
from main import start_me_up


def change_player():
    app = ChangePlayer()
    app.run()


def add_player():
    app = AddPlayer()
    app.run()


def go_back():
    app = SoftwareRender()
    app.run()


def select(prof, score):
    app = SoftwareRender()
    app.run(prof, score)


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
        self.fps_font = pg.font.SysFont('arial', 40)
        self.profile = 'None'
        self.max_score = 0

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
        self.button1.draw()
        self.button2.draw()
        self.screen.blit(
            self.fps_font.render('Сurrent profile: ' + str(self.profile) + '(score: ' + str(self.max_score) + ')', True,
                                 (255, 255, 255)), (10, 20))

    def run(self, prof='None', score=0):
        self.profile = prof
        self.score = score
        self.button = Button(self.screen, 150, 70, 100, 200, 1, start_me_up, "START")
        self.button1 = Button(self.screen, 280, 70, 100, 300, 1, change_player, "Change player")
        self.button2 = Button(self.screen, 215, 70, 100, 400, 1, add_player, "Add player")
        gems = pg.sprite.Group(self.button, self.button1, self.button2)
        while True:
            gems.update(pg.event.get())

            self.draw()
            pg.display.flip()
            self.clock.tick(self.FPS)


class ChangePlayer:
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
        self.button1.draw()
        try:
            self.button2.draw()
            self.button2_r.draw()
            self.button3.draw()
            self.button3_r.draw()
            self.button4.draw()
            self.button4_r.draw()
            self.button5.draw()
            self.button5_r.draw()
            self.button6.draw()
            self.button6_r.draw()
            self.button7.draw()
            self.button7_r.draw()
            self.button8.draw()
            self.button8_r.draw()
        except:
            pass

        self.screen.blit(self.fps_font.render('Select:', True, (255, 255, 255)),
                         (20, 130))

    def buttonf(self, r):
        try:
            self.button2 = Button(self.screen, 300, 70, 20, 200, 1, lambda: select(r[0][0], r[0][1]),
                                  str(r[0][0]) + ': ' + str(r[0][1]))
            self.buttons.add(self.button2)
            self.button2_r = Button(self.screen, 50, 60, 330, 200, (255, 0, 0),
                                    lambda: self.delete_prof(r[0][0], self.button2, self.button2_r), 'X')
            self.buttons.add(self.button2_r)
            self.button3 = Button(self.screen, 300, 70, 20, 280, 1, lambda: select(r[1][0], r[1][1]),
                                  str(r[1][0]) + ': ' + str(r[1][1]))
            self.buttons.add(self.button3)
            self.button3_r = Button(self.screen, 50, 60, 330, 280, (255, 0, 0),
                                    lambda: self.delete_prof(r[1][0], self.button3, self.button3_r), 'X')
            self.buttons.add(self.button3_r)
            self.button4 = Button(self.screen, 300, 70, 20, 360, 1, lambda: select(r[2][0], r[2][1]),
                                  str(r[2][0]) + ': ' + str(r[2][1]))
            self.buttons.add(self.button4)
            self.button4_r = Button(self.screen, 50, 60, 330, 360, (255, 0, 0),
                                    lambda: self.delete_prof(r[2][0], self.button4, self.button4_r), 'X')
            self.buttons.add(self.button4_r)
            self.button5 = Button(self.screen, 300, 70, 20, 440, 1, lambda: select(r[3][0], r[3][1]),
                                  str(r[3][0]) + ': ' + str(r[3][1]))
            self.buttons.add(self.button5)
            self.button5_r = Button(self.screen, 50, 60, 330, 440, (255, 0, 0),
                                    lambda: self.delete_prof(r[3][0], self.button5, self.button5_r), 'X')
            self.buttons.add(self.button5_r)
            self.button6 = Button(self.screen, 300, 70, 20, 520, 1, lambda: select(r[4][0], r[4][1]),
                                  str(r[4][0]) + ': ' + str(r[4][1]))
            self.buttons.add(self.button6)
            self.button6_r = Button(self.screen, 50, 60, 330, 520, (255, 0, 0),
                                    lambda: self.delete_prof(r[4][0], self.button6, self.button6_r), 'X')
            self.buttons.add(self.button6_r)
            self.button7 = Button(self.screen, 300, 70, 20, 600, 1, lambda: select(r[5][0], r[5][1]),
                                  str(r[5][0]) + ': ' + str(r[5][1]))
            self.buttons.add(self.button7)
            self.button7_r = Button(self.screen, 50, 60, 330, 600, (255, 0, 0),
                                    lambda: self.delete_prof(r[5][0], self.button7, self.button7_r), 'X')
            self.buttons.add(self.button7_r)

        except:
            pass

    def run(self):
        self.button1 = Button(self.screen, 170, 70, 20, 20, 1, go_back, 'Go back')
        self.buttons = pg.sprite.Group(self.button1)
        con = sqlite3.connect("players.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM data""").fetchall()
        self.buttonf(result)
        con.close()
        while True:
            self.buttons.update(pg.event.get())
            self.draw()
            pg.display.flip()
            self.clock.tick(self.FPS)

    def delete_prof(self, name, but, but2):
        con = sqlite3.connect("players.db")
        cur = con.cursor()
        cur.execute("DELETE from data WHERE name = \'%s\'" % (name))
        con.commit()
        con.close()
        but.deleteb()
        but2.deleteb()


flag = 0


class AddPlayer:
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
        self.fps_font = pg.font.SysFont('arial', 40)
        self.error_font = pg.font.SysFont('arial', 15)
        con = sqlite3.connect("players.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM data""").fetchall()
        self.count_prof = len(result)
        for elem in result:
            self.profile = elem[0]
            self.max_score = elem[1]
            break
        con.close()

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
        global flag
        self.screen.fill(pg.Color('black'))
        self.plane.rotate_y(np.pi / 360)
        self.fps_show()
        self.plane.draw()
        self.button.draw()
        self.button2.draw()
        self.text_line.draw()
        print(flag)
        if flag == 1:
            self.screen.blit(self.error_font.render('This name is already registered', True, (200, 10, 0)),
                             (20, 330))
        elif flag == 2:
            self.screen.blit(self.error_font.render('allowed number of players exceeded', True, (200, 10, 0)),
                             (20, 350))

    def run(self):
        self.button = Button(self.screen, 170, 70, 20, 20, 1, go_back, 'Go back')
        self.text_line = Textline(self.screen)
        self.button2 = Button(self.screen, 170, 70, 20, 250, 1, lambda: self.add(self.text_line), 'add')
        gems = pg.sprite.Group(self.button, self.button2, self.text_line)
        runn = True
        while runn:
            gems.update(pg.event.get())
            self.draw()
            pg.display.flip()
            self.clock.tick(self.FPS)

    @staticmethod
    def add(text):
        global flag
        con = sqlite3.connect("players.db")
        cur = con.cursor()
        result = cur.execute("""SELECT name FROM data""").fetchall()
        name_list = []
        for i in result:
            name_list.append(str(i[0]))
        if len(result) <= 5:
            if str(text.return_text()) not in name_list:
                if len(text.return_text()) != 0:
                    cur.execute(
                        "INSERT INTO data(name, score) VALUES(\'%s\', \'%s\')" % (str(text.return_text()), 0))
                    con.commit()
                    flag = 0
                    con.close()
                    go_back()
            else:
                flag = 1
        else:
            flag = 2


profile = 'None'
max_score = 0
con = sqlite3.connect("players.db")
cur = con.cursor()
result = cur.execute("""SELECT * FROM data""").fetchall()
for elem in result:
    profile = elem[0]
    max_score = elem[1]
    break
con.close()

app = SoftwareRender()
app.run(profile, max_score)