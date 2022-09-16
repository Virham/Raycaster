from Player import Player
from Raycaster import Raycaster

import random
import time
import pygame
pygame.init()


class Main:
    def __init__(self):
        self.width = 720
        self.height = 720
        self.win = pygame.display.set_mode((self.width, self.height))

        self.map = self.generate_map(100, 100 )
        self.player = Player((-3.2, 2.1), 3, 5, 4, 0.007, self.map)

        self.racaster = Raycaster(self, self.map, self.player, 100, 60, 15)

        self.time = time.time()

        pygame.mouse.set_visible(False)

        self.perspective = True

    def generate_map(self, width, height):
        map = []

        for i in range(width):
            for j in range(height):
                if random.randint(0, 3 ) == 0:
                    map.append((i, j))

        return map

    def draw(self):
        self.racaster.draw_persepctive(self.win) if self.perspective else self.racaster.draw(self.win)

        pygame.display.update()

    def get_dt(self):
        now = time.time()
        dt = now - self.time
        self.time = now
        return dt

    def update(self, dt):
        self.player.update(dt)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.perspective = not self.perspective

            self.player.event_handler(event)

            self.update(self.get_dt())
            self.draw()

            pygame.mouse.set_pos(self.width / 2, self.height / 2)



Main().loop()

