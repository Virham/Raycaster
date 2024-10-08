import math
import pygame


class Raycaster:
    def __init__(self, main, map, player, resolution, fov, render_distance):
        self.main = main
        self.map = map
        self.player = player

        self.resolution = resolution
        self.fov = fov / 180 * math.pi
        self.render_distance = render_distance

        self.scale = 50

    def cast_rays(self):
        angle_incr = self.fov / self.resolution
        start = self.player.angle - self.fov / 2
        results = [None] * self.resolution

        for i in range(self.resolution):
            angle = start + angle_incr * i
            results[i] = self.raycast(self.player.pos, angle)

        return results

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

    def raycast(self, pos, angle):
        direction = (math.cos(angle), math.sin(angle))

        sc_x = math.sqrt(1 + (direction[1] / direction[0]) ** 2) if direction[0] else 1
        sc_y = math.sqrt(1 + (direction[0] / direction[1]) ** 2) if direction[1] else 1

        side = 0
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
                side = (self.sign(direction[0]) + 1) // 2
            else:
                intersection = (intersection[0] + y * sc_y * direction[0], round(intersection[1] + y * self.sign(direction[1])))
                length += y * sc_y
                block = (block[0], block[1] + self.sign(direction[1]))
                side = (self.sign(direction[1]) + 1) // 2 + 2

            if block in self.map:
                better_len = length * math.cos(self.player.angle - angle) if self.main.perspective else length
                return better_len, intersection, side

        return length, False, side

    def draw_raycast(self, win):
        angle_incr = self.fov / self.resolution
        start = self.player.angle - self.fov / 2

        for i in range(self.resolution):
            angle = start + angle_incr * i
            x = win.get_width() / 2
            y = win.get_height() / 2
            mag, intersection, side = self.raycast(self.player.pos, angle)
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
        res = self.cast_rays()

        height = win.get_height() / 2 + self.player.y

        pygame.draw.rect(win, (64, 128, 255), (0, 0, win.get_width(), height))
        pygame.draw.rect(win, (229, 229, 190), (0, height, win.get_width(), win.get_height() - height))

        for i, v in enumerate(res):
            if v[1]:
                normalized = min(1, v[0] / self.render_distance)
                w = win.get_width() / self.resolution
                x = w * i
                h = win.get_height() / v[0]
                y = (win.get_height() - h) / 2 + self.player.y / normalized

                sat = (1 - normalized) * 0.45 + 0.55
                color = (128, 0, 0) if not v[2] >= 2 else (255, 0, 0)

                pygame.draw.rect(win, (color[0] * sat, color[1] * sat, color[2] * sat), (x, y, w+1, h))
