import pygame as pg
from numba import njit

from working.matrix_functions import *


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, vertexes='', faces='', color_mode=1):
        self.render = render
        self.start_pos = vertexes[0]
        self.vertexes = np.array([np.array(v) for v in vertexes])
        self.faces = np.array([np.array(face) for face in faces])
        self.translate([0.0001, 0.0001, 0.0001])

        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag, self.draw_vertexes = True, False
        self.label = ''
        self.color = [255, 0, 0]
        self.dir = True
        self.color_mode = color_mode

        if self.color_mode == 2:
            self.color = [150, 150, 150]
        if self.color_mode == 3:
            self.color = [0, 204, 255]

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
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

        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertexes[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                """if self.color_mode == 2:
                    pg.draw.polygon(self.render.screen, (255, 255, 255), polygon)"""
                pg.draw.polygon(self.render.screen, self.color, polygon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])

        if self.draw_vertexes:
            for vertex in vertexes:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)


class Plane(Object3D):
    def __init__(self, render, vertexes='', faces='', color_mode=1):
        super().__init__(render, vertexes, faces, color_mode)
        self.render = render
        self.start_pos = [sum(i) / len(vertexes) for i in
                          np.array(vertexes).transpose() * np.array([1, 1, 1, 1]).reshape(1, 4).transpose()]
        self.max_angle = np.pi / 7
        self.real_angle = 0
        self.vertexes = np.array([np.array(v) for v in vertexes])
        self.faces = np.array([np.array(face) for face in faces])
        self.translate([0.0001, 0.0001, 0.0001])

        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag, self.draw_vertexes = True, False
        self.label = ''
        self.color = [255, 0, 0]
        self.dir = True
        self.color_mode = color_mode

        if self.color_mode == 2:
            self.color = [150, 150, 150]
        if self.color_mode == 3:
            self.color = [0, 204, 255]

    def draw(self):
        self.screen_projection()

    def matrix_rotate(self):
        point = [sum(i) / len(self.vertexes) for i in
                 np.array(self.vertexes).transpose() * np.array([1, 1, 1, 1]).reshape(1,
                                                                                      4).transpose()]
        step = (np.array(np.array(point) - self.start_pos)).transpose()
        return step

    def rotate_x(self, angle):
        step = self.matrix_rotate()
        self.vertexes = self.vertexes - step
        self.vertexes = self.vertexes @ rotate_x(angle)
        self.vertexes = self.vertexes + step

    def rotate_y(self, angle):
        step = self.matrix_rotate()
        self.vertexes = self.vertexes - step
        self.vertexes = self.vertexes @ rotate_y(angle)
        self.vertexes = self.vertexes + step

    def rotate_z(self, angle):
        step = self.matrix_rotate()
        self.vertexes = self.vertexes - step
        self.vertexes = self.vertexes @ rotate_z(angle)
        self.vertexes = self.vertexes + step


class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertexes = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertexes = False
        self.label = 'XYZ'


class Coin(Plane):
    pass
