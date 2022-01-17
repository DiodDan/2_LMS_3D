import sqlite3

from settings import *
from working.camera import *
from working.object_3d import *
from working.projection import *
from working import render
from working.ui_items import Button, Textline
from main import start_me_up


def change_player():
    app_change = ChangePlayer()
    app_change.run()


def add_player():
    app_add = AddPlayer()
    app_add.run()


def go_back():
    app_back = SoftwareRender()
    app_back.run()


def delete_prof(name, but, but2):
    connect = sqlite3.connect("players.db")
    curs = connect.cursor()
    curs.execute(f"DELETE from data WHERE name = \'{name}\'")
    connect.commit()
    connect.close()
    but.deleteb()
    but2.deleteb()


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


def select(prof, score):
    app_select = SoftwareRender()
    app_select.run(prof, score)


class SoftwareRender:
    def __init__(self):
        self.plane = None
        self.score = None
        self.button = None
        self.button1 = None
        self.button2 = None
        pg.init()
        self.objects = []
        self.RES = self.WIDTH, self.HEIGHT = height, width
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
        self.plane = Plane(self, *get_object_from_file('objects/Plane_low.obj'), color_mode=1)
        self.plane.rotate_y(np.pi / 2)
        self.plane.rotate_x(np.pi)
        self.plane.translate([0, 50, -300])

    def fps_show(self):
        self.screen.blit(self.fps_font.render(str(int(self.clock.get_fps())), True, (255, 255, 255)),
                         (self.WIDTH - 80, 20))

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.plane.rotate_y(np.pi / 360)
        self.fps_show()
        self.plane.draw()
        self.button.draw()
        self.button1.draw()
        self.button2.draw()
        self.screen.blit(
            self.fps_font.render('Сurrent profile: ' + str(self.profile), True,
                                 (255, 255, 255)), (10, 20))

    def run(self, prof='None', score=0):
        self.profile = prof
        self.score = score

        self.button = Button(self.screen, 150, 70, 100, 200, 1, lambda: start_me_up(self.profile), "START")
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
        self.buttons = None
        self.button1 = None
        self.plane = None
        pg.init()
        self.objects = []
        self.RES = self.WIDTH, self.HEIGHT = height - 50, width - 90
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = FPS
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()
        self.buttons_data = []
        self.camera = Camera(self, [10, 0, -100])
        self.projection = Projection(self)
        self.fps_font = pg.font.SysFont('arial', 40)

    def create_objects(self):
        self.plane = Plane(self, *get_object_from_file('objects/Plane_low.obj'), color_mode=1)
        self.plane.rotate_y(np.pi / 2)
        self.plane.rotate_x(np.pi)
        self.plane.translate([0, 50, -300])

    def fps_show(self):
        self.screen.blit(self.fps_font.render(str(int(self.clock.get_fps())), True, (255, 255, 255)),
                         (self.WIDTH - 80, 20))

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.plane.rotate_y(np.pi / 360)
        self.fps_show()
        self.plane.draw()
        self.button1.draw()
        for el in self.buttons_data:
            el.draw()

        self.screen.blit(self.fps_font.render('Select:', True, (255, 255, 255)),
                         (20, 130))

    def button_create(self, r):
        for i in range(len(r)):
            button_temp = Button(self.screen, 300, 70, 20, 200 + 80 * i, 1, lambda: select(r[i][0], r[i][1]),
                                 str(r[i][0]) + ': ' + str(r[i][1]))
            self.buttons.add(button_temp)
            self.buttons_data.append(button_temp)
            j = i
            if i % 2 != 0:
                j = i + 1
            button_temp_delete = Button(self.screen, 50, 60, 330, 200 + 80 * i, (255, 0, 0),
                                        lambda: delete_prof(r[i][0], self.buttons_data[j],
                                                            self.buttons_data[j + 1]),
                                        'X')
            self.buttons.add(button_temp_delete)
            self.buttons_data.append(button_temp_delete)

    def run(self):
        self.button1 = Button(self.screen, 170, 70, 20, 20, 1, go_back, 'Go back')
        self.buttons = pg.sprite.Group(self.button1)
        connection = sqlite3.connect("players.db")
        cursor = connection.cursor()
        result_fetching = cursor.execute("""SELECT * FROM data""").fetchall()
        self.button_create(result_fetching)
        con.close()
        while True:
            self.buttons.update(pg.event.get())
            self.draw()
            pg.display.flip()
            self.clock.tick(self.FPS)


flag = 0


class AddPlayer:
    def __init__(self):
        self.button2 = None
        self.button = None
        self.plane = None
        self.text_line = None
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
        conn = sqlite3.connect("players.db")
        curr = conn.cursor()
        result_data = curr.execute("""SELECT * FROM data""").fetchall()
        self.count_prof = len(result_data)
        for elem in result_data:
            self.profile = elem[0]
            self.max_score = elem[1]
            break
        con.close()

    def create_objects(self):
        self.plane = Plane(self, *get_object_from_file('objects/Plane_low.obj'), color_mode=1)
        self.plane.rotate_y(np.pi / 2)
        self.plane.rotate_x(np.pi)
        self.plane.translate([0, 50, -300])

    def fps_show(self):
        self.screen.blit(self.fps_font.render(str(int(self.clock.get_fps())), True, (255, 255, 255)),
                         (self.WIDTH - 80, 20))

    def draw(self):
        global flag
        self.screen.fill(pg.Color('black'))
        self.plane.rotate_y(np.pi / 360)
        self.fps_show()
        self.plane.draw()
        self.button.draw()
        self.button2.draw()
        self.text_line.draw()
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
        while True:
            gems.update(pg.event.get())
            self.draw()
            pg.display.flip()
            self.clock.tick(self.FPS)

    @staticmethod
    def add(text):
        global flag
        connect = sqlite3.connect("players.db")
        curs = connect.cursor()
        results = curs.execute("""SELECT name FROM data""").fetchall()
        name_list = []
        for i in results:
            name_list.append(str(i[0]))
        if len(results) <= 5:
            if str(text.return_text()) not in name_list:
                if len(text.return_text()) != 0:
                    curs.execute(
                        "INSERT INTO data(name, score) VALUES(\'%s\', \'%s\')" % (str(text.return_text()), 0))
                    connect.commit()
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
