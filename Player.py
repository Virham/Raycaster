import pygame
import math


class Player:
    def __init__(self, pos, move_speed, sprint_speed, angle_speed, mouse_speed, map):
        self.pos = pos
        self.angle = 0.1

        self.move_speed = move_speed
        self.sprint_speed = sprint_speed
        self.angle_speed = angle_speed
        self.mouse_speed = mouse_speed
        self.map = map

        self.y = 0
        self.vel = 0

    @property
    def keys(self):
        return pygame.key.get_pressed()

    def event_handler(self, event):
        if event.type == pygame.MOUSEMOTION:
            x = event.pos[0] - pygame.display.get_surface().get_width() / 2
            y = event.pos[1] - pygame.display.get_surface().get_height() / 2
            self.angle += x * self.mouse_speed

    def get_look_direction(self):
        return math.cos(self.angle), math.sin(self.angle)

    def get_right_direction(self):
        right = self.angle + math.pi / 2
        return math.cos(right), math.sin(right)

    def sign(self, x):
        if x > 0:
            return 1
        if x < 0:
            return -1
        return 0

    def move(self, dt):
        move_speed = self.move_speed if not self.keys[pygame.K_LSHIFT] else self.sprint_speed

        right_axis = self.keys[pygame.K_d] - self.keys[pygame.K_a]
        forward_axis = self.keys[pygame.K_w]- self.keys[pygame.K_s]

        forward_dir = self.get_look_direction()
        right_dir = self.get_right_direction()

        forward = (forward_dir[0] * forward_axis, forward_dir[1] * forward_axis)
        right = (right_dir[0] * right_axis, right_dir[1] * right_axis)

        vel = ((forward[0] + right[0]) * dt * move_speed, (forward[1] + right[1]) * dt * move_speed)
        if right_axis and forward_axis:
            mag = math.sqrt(2)
            vel = (vel[0] / mag, vel[1] / mag)

        x = self.pos[0] + vel[0]
        y = self.pos[1] + vel[1]

        if (math.floor(x), math.floor(y)) in self.map:
            if (math.floor(self.pos[0]), math.floor(y)) in self.map:
                y = self.pos[1]
            if (math.floor(x), math.floor(self.pos[1])) in self.map:
                x = self.pos[0]

        current = (math.floor(self.pos[0]), math.floor(self.pos[1]))
        next = (math.floor(x), math.floor(y))

        if next not in self.map:
            if current[0] != next[0] and current[1] != next[1]:
                if (current[0] + self.sign(next[0] - current[0]), current[1]) in self.map:
                    if (current[0], current[1] + self.sign(next[1] - current[1])) in self.map:
                        return

        self.pos = (x, y)

        self.jump(dt)

    def jump(self, dt):
        if not self.y and self.keys[pygame.K_SPACE]:
            self.vel = 100

        self.y += self.vel * dt
        if self.vel:
            self.vel -= 300 * dt

        if self.y < 0:
            self.vel = 0
            self.y = 0

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
