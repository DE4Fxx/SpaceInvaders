import pygame
import bullet
import random
from constants import *


ENEMY_PATH = "assets\enemyship.png"

class Enemy:

    __slots__ = ["surface","bullets","hp","rect"]

    def __init__(self, min, max, player_x):
        self.surface = pygame.image.load(ENEMY_PATH)
        self.surface = pygame.transform.scale(self.surface, (ENEMY_SIZE, ENEMY_SIZE))  # Resize the image
        self.rect = self.surface.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - player_x)
        self.rect.y = random.randint(0, 100)
        self.hp = random.randint(min, max)


    def y(self):
        return self.rect.y
    
    def x(self):
        return self.rect.x

    def get_rect(self):
        return self.rect
    
    def get_surface(self):
        return self.surface
    
    def get_hp(self):
        return self.hp
    
    def reduce_hp(self, damage):
        self.hp -= damage

    def move(self,speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def shoot(self):
            bullet_x = self.rect.centerx
            bullet_y = self.rect.bottom
            bullet_width = 5
            bullet_height = 5
            bullet_speed = 7
            return bullet.Bullet(bullet_x, bullet_y, bullet_width, bullet_height, bullet_speed)
        
    def has_line_of_sight(self, player_rect, obstacles):
        # Check if player is horizontally aligned with the enemy
        if self.rect.left < player_rect.centerx < self.rect.right:
            # Determine the vertical range
            top, bottom = sorted([self.rect.bottom, player_rect.top])

            for obstacle in obstacles:
                # Check if the obstacle is within the vertical range and horizontally overlaps the enemy
                if top < obstacle.bottom and bottom > obstacle.top and \
                obstacle.left < self.rect.centerx < obstacle.right:
                    return False
            return True
        return False