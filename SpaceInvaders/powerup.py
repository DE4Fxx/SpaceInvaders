import pygame
import random

class PowerUp:
    __slots__ = ["color", "type", "rect", "active_duration","speed"]

    def __init__(self, x, y, width, height, powerup_type):
        self.type = powerup_type
        self.rect = pygame.Rect(x, y, width, height)
        self.active_duration = 5000 
        self.speed = 4
        if(self.type == "heal"):
            self.color = (255, 255, 0)
        elif(self.type == "spread"):
            self.color = (0,0,255)

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)