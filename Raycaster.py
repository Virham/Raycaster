import math
import pygame


class Raycaster:
    def __init__(self, map, player, resolution, fov, render_distance):
        self.map = map
        self.player = player

        self.resolution = resolution
        self.fov = fov / 180 * math.pi
        self.render_distance = render_distance

    def cast_rays(self):
        angle_incr = self.fov / self.resolution
        start = self.player.angle - self.fov / 2

        for i in range(self.resolution):
            angle = start + angle_incr * i
            x = math.cos(angle)
            y = math.sin(angle)
            self.raycast(self.player.pos, (x * self.render_distance, y * self.render_distance))

    def sign(self, x):
        if x > 0:
            return 1
        if x < 0:
            return -1
        return 0

    def raycast(self, pos, direction):
        u = abs(math.atan(direction[0] / direction[1]))
        x = (pos[0] * -self.sign(direction[0])) % 1 if pos[0] % 1 else self.sign(direction[0])
        y = (pos[1] * -self.sign(direction[1])) % 1 if pos[1] % 1 else self.sign(direction[1])

        x_mag = x * math.cos(u)
        y_mag = y * math.sin(u)

        mag = min(x_mag, y_mag)

        return abs(mag)

    def draw_raycast(self, win):
        angle_incr = self.fov / self.resolution
        start = self.player.angle - self.fov / 2

        for i in range(self.resolution):
            angle = start + angle_incr * i
            x = win.get_width() / 2
            y = win.get_height() / 2
            mag = self.raycast((x / 75, y / 75), (math.cos(angle), math.sin(angle))) * 200
            pygame.draw.line(win, (0, 255, 0), (x, y), (x + math.cos(angle) * mag, y + math.sin(angle) * mag))

    def draw(self, win):
        win.fill(255)
        res = 75

        off_x = self.player.pos[0] - win.get_width() / 2
        off_y = self.player.pos[1] - win.get_height() / 2

        for i in self.map:
            pygame.draw.rect(win, (0, 0, 0), (i[0] * res - off_x, i[1] * res - off_y, res, res))

        self.player.draw(win)
        self.draw_raycast(win)