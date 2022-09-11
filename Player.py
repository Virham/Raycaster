import pygame
import math


class Player:
    def __init__(self, pos, move_speed, angle_speed):
        self.pos = pos
        self.angle = 0

        self.move_speed = move_speed
        self.angle_speed = angle_speed

    @property
    def keys(self):
        return pygame.key.get_pressed()

    def get_look_direction(self):
        return math.cos(self.angle), math.sin(self.angle)

    def get_right_direction(self):
        right = self.angle + math.pi / 2
        return math.cos(right), math.sin(right)

    def move(self, dt):
        right_axis = self.keys[pygame.K_d] - self.keys[pygame.K_a]
        forward_axis = self.keys[pygame.K_w]- self.keys[pygame.K_s]

        forward_dir = self.get_look_direction()
        right_dir = self.get_right_direction()

        forward = (forward_dir[0] * forward_axis, forward_dir[1] * forward_axis)
        right = (right_dir[0] * right_axis, right_dir[1] * right_axis)

        vel = ((forward[0] + right[0]) * dt * self.move_speed, (forward[1] + right[1]) * dt * self.move_speed)
        if right_axis and forward_axis:
            mag = math.sqrt(2)
            vel = (vel[0] / mag, vel[1] / mag)

        x = self.pos[0] + vel[0]
        y = self.pos[1] + vel[1]
        self.pos = (x, y)

    def rotate(self, dt):
        dir = self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT]
        self.angle += dir * self.angle_speed * dt

    def update(self, dt):
        self.rotate(dt)
        self.move(dt)

    def draw(self, win):
        dir = self.get_look_direction()

        width = win.get_width() / 2
        height = win.get_height() / 2

        pygame.draw.circle(win, (255, 0, 0), (width, height), 5)
        pygame.draw.line(win, (0, 255, 0), (width, height), (width + dir[0] * 10, height + dir[1] * 10))
