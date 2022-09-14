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
        self.player = Player((-3.2, 2.1), 3, 5, 4, self.map)

        self.racaster = Raycaster(self.map, self.player, 100, 60, 10)

        self.time = time.time()

    def generate_map(self, width, height):
        map = []

        for i in range(width):
            for j in range(height):
                if random.randint(0, 3 ) == 0:
                    map.append((i, j))

        return map

    def draw(self):
        self.racaster.draw_persepctive(self.win)

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

            self.update(self.get_dt())
            self.draw()


Main().loop()

