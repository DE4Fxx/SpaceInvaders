import pygame
import random
from constants import *

class PowerUp:
    __slots__ = ["color","x","y", "type","image", "rect", "active_duration","speed"]

    def __init__(self, x, y, powerup_type):
        self.type = powerup_type
        if self.type == "heal":
            self.image = HEALTH

        elif self.type == "spread":
            self.image = BULLET
        self.rect = self.image.get_rect()

        self.active_duration = 5000 
        self.speed = 4
        if(self.type == "heal"):
            self.color = (255, 255, 0)
        elif(self.type == "spread"):
            self.color = (0,0,255)
        self.x = x
        self.y = y

    def move(self):
        self.y += self.speed


    def get_rect(self):
        return self.rect
    
    def collide(self,player):
        if self.rect.colliderect(player):
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image,(self.x,self.y))
        self.rect.x = self.x
        self.rect.y = self.y