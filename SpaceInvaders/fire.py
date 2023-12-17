import pygame
import random

class Flame:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_velocity = random.uniform(-0.5, 0.5)
        self.y_velocity = random.uniform(-1, -3)
        self.lifetime = random.randint(30, 60)
        self.size = random.randint(3, 6)
        self.color = (255, random.randint(100, 150), 0)  # Initial orange-red color

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.lifetime -= 1

        # Color transition from yellow to red
        red = 255
        green = min(255, self.color[1] + 2)
        blue = 0

        # Fade effect
        if self.lifetime < 20:
            alpha = int(255 * (self.lifetime / 20))
            red, green = max(0, red - (255 - alpha)), max(0, green - (255 - alpha))

        self.color = (red, green, blue)
        self.size = max(1, self.size - 0.1)  # Gradually decrease size

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
