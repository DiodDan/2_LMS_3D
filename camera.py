import pygame as pg
from matrix_functions import *

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
        self.moving_speed = 10
        self.rotation_speed = 0.02
        self.camera_moovex(0.3)

    def control(self):
        key = pg.key.get_pressed()
        self.position += np.array([0, 0, 1, 1]).transpose() * self.moving_speed
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
            self.render.plane.translate(-self.right[0:3] * self.moving_speed)
            if self.render.plane.max_angle >= np.abs(self.render.plane.real_angle):
                self.render.plane.rotate_z(np.pi / 200)
                self.render.plane.real_angle -= np.pi / 200

        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
            self.render.plane.translate(self.right[0:3] * self.moving_speed)
            if self.render.plane.max_angle >= np.abs(self.render.plane.real_angle):
                self.render.plane.rotate_z(-np.pi / 200)
                self.render.plane.real_angle -= -np.pi / 200
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_moovey(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_moovey(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_moovex(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_moovex(self.rotation_speed)

        if key[pg.K_m]:
            self.camera_moovez(-self.rotation_speed)
        if key[pg.K_n]:
            self.camera_moovez(self.rotation_speed)

    def camera_moovey(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_moovex(self, angle):
        rotate = rotate_x(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_moovez(self, angle):
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