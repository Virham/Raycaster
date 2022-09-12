import math
import pygame


class Raycaster:
    def __init__(self, map, player, resolution, fov, render_distance):
        self.map = map
        self.player = player

        self.resolution = resolution
        self.fov = fov / 180 * math.pi
        self.render_distance = render_distance

        self.scale = 50

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

    def get_offset(self, pos, dir):
        if not pos % 1:
            return 1
        if dir > 0:
            return 1 - pos % 1
        return pos % 1

    def raycast(self, pos, direction):
        sc_x = math.sqrt(1 + (direction[1] / direction[0]) ** 2) if direction[0] else 1
        sc_y = math.sqrt(1 + (direction[0] / direction[1]) ** 2) if direction[1] else 1

        intersection = pos
        length = 0
        block = (math.floor(pos[0]), math.floor(pos[1]))

        while length < self.render_distance:
            x = self.get_offset(intersection[0], direction[0])
            y = self.get_offset(intersection[1], direction[1])
            if x * sc_x < y * sc_y:
                intersection = (round(intersection[0] + x * self.sign(direction[0])), intersection[1] + x * sc_x * direction[1])
                length += x * sc_x
                block = (block[0] + self.sign(direction[0]), block[1])
            else:
                intersection = (intersection[0] + y * sc_y * direction[0], round(intersection[1] + y * self.sign(direction[1])))
                length += y * sc_y
                block = (block[0], block[1] + self.sign(direction[1]))

            if block in self.map:
                return length, intersection

        return length, False

    def draw_raycast(self, win):
        angle_incr = self.fov / self.resolution
        start = self.player.angle - self.fov / 2

        for i in range(self.resolution):
            angle = start + angle_incr * i
            x = win.get_width() / 2
            y = win.get_height() / 2
            mag, intersection = self.raycast(self.player.pos, (math.cos(angle), math.sin(angle)))
            mag *= self.scale

            if intersection:
                pygame.draw.line(win, (0, 255, 0), (x, y), (x + math.cos(angle) * mag, y + math.sin(angle) * mag), 3)

    def draw(self, win):
        win.fill(255)

        off_x = self.player.pos[0] * self.scale - win.get_width() / 2
        off_y = self.player.pos[1] * self.scale- win.get_height() / 2

        for i in self.map:
            pygame.draw.rect(win, (0, 0, 0), (i[0] * self.scale - off_x, i[1] * self.scale - off_y, self.scale, self.scale))

        self.player.draw(win)
        self.draw_raycast(win)

    def draw_persepctive(self, win):
        win.fill((0, 0, 0))

        angle_incr = self.fov / self.resolution
        start = self.player.angle - self.fov / 2

        for i in range(self.resolution):
            angle = start + angle_incr * i
            x = math.cos(angle)
            y = math.sin(angle)
            length, hit_point = self.raycast(self.player.pos, (x * self.render_distance, y * self.render_distance))

            if hit_point:
                normalized = self.render_distance / length
                x = win.get_width() / self.resolution * i
                y = win.get_height() / 2 - normalized * 50
                w = win.get_width() / self.resolution
                h = normalized * 100

                pygame.draw.rect(win, (0, 0, 255), (x, y, w, h))