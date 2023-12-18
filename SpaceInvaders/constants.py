import pygame

PLAYER_IMAGE = "assets/spaceship.1.png"
NEGATIVE_IMAGE = "assets/spaceship_negative.png"
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ENEMY_SIZE = 40
PLAYER_SIZE = 40
BULLET_SIZE = 5
ENEMY_SPEED = 5
GREEN = (0,255,0)
BULLET_SPEED = 10
BACKGROUND_IMAGE = "assets/bg.jpg"
OBS_SPAWN_INTERVAL = 200
ENEMY_INTERVAL = 150
OBS_INTERVAL = 50
OBSTACLE_DAMAGE = 9
POWER_UP_INTERVAL = 100
SPREAD_INTERVAL = 750
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 36)
POWER_UP_TYPES = ["heal","spread"]
