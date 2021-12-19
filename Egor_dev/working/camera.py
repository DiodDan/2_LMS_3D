import pygame as pg

from working.matrix_functions import *
from settings import flip_speed, moving_speed, rotation_speed, cam_start_angle, follow_moving_speed


class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = moving_speed
        self.rotation_speed = rotation_speed
        self.camera_move_on_x(cam_start_angle)

    def control(self):
        key = pg.key.get_pressed()
        self.position += np.array([0, 0, 1, 1]).transpose() * follow_moving_speed
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
            self.render.plane.translate(-self.right[0:3] * self.moving_speed)
            if self.render.plane.max_angle >= np.abs(self.render.plane.real_angle):
                self.render.plane.rotate_z(np.pi / flip_speed)
                self.render.plane.real_angle -= np.pi / flip_speed

        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
            self.render.plane.translate(self.right[0:3] * self.moving_speed)
            if self.render.plane.max_angle >= np.abs(self.render.plane.real_angle):
                self.render.plane.rotate_z(-np.pi / flip_speed)
                self.render.plane.real_angle -= -np.pi / flip_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_move_on_y(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_move_on_y(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_move_on_x(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_move_on_x(self.rotation_speed)

        if key[pg.K_m]:
            self.camera_move_on_z(-self.rotation_speed)
        if key[pg.K_n]:
            self.camera_move_on_z(self.rotation_speed)

    def camera_move_on_y(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_move_on_x(self, angle):
        rotate = rotate_x(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_move_on_z(self, angle):
        rotate = rotate_z(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()