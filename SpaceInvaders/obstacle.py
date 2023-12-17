import pygame
import random
from constants import *

OBSTACLE_SIZE = 25
ASTEROID_PATH = "assets/asteroid.png"

class Obstacle:

    def __init__(self,speed):
        self.surface = pygame.image.load(ASTEROID_PATH)
        self.surface = pygame.transform.scale(self.surface, (OBSTACLE_SIZE, OBSTACLE_SIZE))  # Resize the image
        self.rect = self.surface.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect.y = random.randint(0, 50)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def get_rect(self):
        return self.rect

    def collided_with_player(self,player):
        if self.rect.colliderect(player):
            return True
        return False

    def draw(self, screen):
        screen.blit(self.surface,self.rect)