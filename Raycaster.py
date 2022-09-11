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
            print(self.player.pos)
            self.raycast(self.player.pos, (x * self.render_distance, y * self.render_distance))

    def sign(self, x):
        if x > 0:
            return 1
        if x < 0:
            return -1
        return 0

    def start_length(self, pos, dir):
        return (dir > 0) - pos % 1

    def raycast(self, pos, direction):
        start_x = self.start_length(pos[0], direction[0])
        start_y = self.start_length(pos[1], direction[1])

        sc_x = math.sqrt(1 + (direction[0] / direction[1]) ** 2 if direction[1] else 0)
        sc_y = math.sqrt(1 + (direction[1] / direction[0]) ** 2 if direction[0] else 0)

        return min(sc_x, sc_y)

    def draw_raycast(self, win):
        angle_incr = self.fov / self.resolution
        start = self.player.angle - self.fov / 2

        for i in range(self.resolution):
            angle = start + angle_incr * i
            x = win.get_width() / 2
            y = win.get_height() / 2
            mag = self.raycast(self.player.pos, (math.cos(angle), math.sin(angle))) * 75 / 2
            pygame.draw.line(win, (0, 255, 0), (x, y), (x + math.cos(angle) * mag, y + math.sin(angle) * mag))

    def draw(self, win):
        win.fill(255)
        res = 75

        off_x = self.player.pos[0] * res - win.get_width() / 2
        off_y = self.player.pos[1] * res - win.get_height() / 2

        for i in self.map:
            pygame.draw.rect(win, (0, 0, 0), (i[0] * res - off_x, i[1] * res - off_y, res, res))

        self.player.draw(win)
        self.draw_raycast(win)