import pygame
import random

class Particle:
    def __init__(self, x, y,color):
        self.x = x
        self.y = y
        self.size = random.randint(1, 4)
        self.color = color # Green color for health effect
        self.lifetime = random.randint(20, 50)  # Frames before the particle disappears
        self.x_vel = random.uniform(-1, 1)  # Horizontal velocity
        self.y_vel = random.uniform(-1, 1)  # Vertical velocity

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.lifetime -= 1  # Decrease lifetime each frame

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)