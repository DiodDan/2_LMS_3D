import pygame as pg

class Button:
    def __init__(self, screen, size_x, size_y, point_x, point_y, color_mode, onClick, text):
        pg.init()
        self.screen = screen
        self.size_x = size_x
        self.size_y = size_y
        self.onClick = onClick
        self.point_x = point_x
        self.point_y = point_y
        self.color_mode = color_mode
        self.color = [255, 0, 0]
        self.width = 4
        self.border_radius = 2
        self.dir = True
        self.text = text
        self.font = pg.font.SysFont('arial', 40)


    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEMOTION:
                if self.point_x < event.pos[0] < self.size_x + self.point_x and self.point_y < event.pos[1] < self.size_y + self.point_y:
                    self.is_hovered = True
                else:
                    self.is_hovered = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.point_x < event.pos[0] < self.size_x + self.point_x and self.point_y < event.pos[1] < self.size_y + self.point_y:
                    self.onClick()


            elif event.type == pg.QUIT:
                quit()


    def draw(self):
        self.change_color()

        if not self.is_hovered:
            self.screen.blit(self.font.render(self.text, True, self.color),
                             (self.point_x + 10, self.point_y + 10))
            pg.draw.rect(self.screen, self.color, (self.point_x, self.point_y, self.size_x, self.size_y), width=self.width, border_radius=self.border_radius)
        else:
            pg.draw.rect(self.screen, self.color, (self.point_x, self.point_y, self.size_x, self.size_y), border_radius=self.border_radius)
            self.screen.blit(self.font.render(self.text, True, (0, 0, 0)), (self.point_x + 10, self.point_y + 10))

    def change_color(self):
        if self.color_mode == 1:
            if self.dir and self.color[2] != 255:
                self.color[2] += 1
            elif self.color[2] == 255 and self.color[0] == 0:
                self.dir = False
            elif self.dir:
                self.color[0] -= 1

            if not self.dir and self.color[0] != 255:
                self.color[0] += 1
            elif self.color[0] == 255 and self.color[2] == 0:
                self.dir = True
            elif not self.dir:
                self.color[2] -= 1