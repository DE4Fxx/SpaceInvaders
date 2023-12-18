import pygame


class Bullet:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def get_y(self):
        return self.rect.y

    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect)  # Draw bullet as red rectangle

    def collide_rect(self,player):
        return self.rect.colliderect(player)