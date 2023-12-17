import pygame
import random


class Flame:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_velocity = random.uniform(-1, 1)
        self.y_velocity = random.uniform(-3, 0)
        self.lifetime = random.randint(20, 70)
        self.color = (255, random.randint(100, 150), 0) # Orange-red color

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.lifetime -= 1
        self.color = (random.randint(200,255), random.randint(100, 150), random.randint(50,75))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
