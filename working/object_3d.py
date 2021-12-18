import pygame as pg
from numba import njit
from settings import draw_vertexes

from working.matrix_functions import *
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

@njit
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, vertexes='', faces='', color_mode=1):
        self.render = render
        self.start_pos = vertexes[0]
        self.vertexes = np.array(vertexes)
        self.faces = np.array(faces)
        self.translate([0.0001, 0.0001, 0.0001])
        self.color = [255, 0, 0]
        self.dir = True
        self.color_mode = color_mode
        self.line_size = 1

        if self.color_mode == 2:
            self.color = [150, 150, 150]
        if self.color_mode == 3:
            self.color = [0, 204, 255]

    def draw(self):
        self.screen_projection()

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

    def screen_projection(self):
        self.change_color()
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for face in self.faces:
            polygon = vertexes[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                """if self.color_mode == 2:
                    pg.draw.polygon(self.render.screen, (255, 255, 255), polygon)"""
                pg.draw.polygon(self.render.screen, self.color, polygon, self.line_size)

        if draw_vertexes:
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
        self.max_angle = np.pi / 7
        self.real_angle = 0
        self.line_size = 4

        self.movement_flag, self.draw_vertexes = True, False
        self.label = ''
        self.color = [255, 0, 0]
        self.dir = True
        self.color_mode = color_mode

        if self.color_mode == 2:
            self.color = [150, 150, 150]
        if self.color_mode == 3:
            self.color = [0, 204, 255]

    def step_calculation(self):
        point = [sum(i) / len(self.vertexes) for i in np.array(self.vertexes).transpose() * np.array([1, 1, 1, 1]).reshape(1, 4).transpose()]
        step = np.array(point).transpose()
        return step

    def rotate_x(self, angle):
        step = self.step_calculation()
        self.vertexes = self.vertexes - step
        self.vertexes = self.vertexes @ rotate_x(angle)
        self.vertexes = self.vertexes + step

    def rotate_y(self, angle):
        step = self.step_calculation()
        self.vertexes = self.vertexes - step
        self.vertexes = self.vertexes @ rotate_y(angle)
        self.vertexes = self.vertexes + step

    def rotate_z(self, angle):
        step = self.step_calculation()
        self.vertexes = self.vertexes - step
        self.vertexes = self.vertexes @ rotate_z(angle)
        self.vertexes = self.vertexes + step



class Coin(Plane):
    pass
