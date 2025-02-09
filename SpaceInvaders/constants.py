import pygame

pygame.init()
PLAYER_IMAGE = "assets/spaceship.1.png"
NEGATIVE_IMAGE = "assets/spaceship_negative.png"
FONT_PATH = "assets/slkscrb.ttf"
ENEMY_SIZE = 120
PLAYER_SIZE = 80
BULLET_SIZE = 5
ENEMY_SPEED = 3.5
FONT_COLORS = [(75,150,255),(0, 255, 0)]
GREEN = (0,255,0)
BULLET_SPEED = 10
BACKGROUND_IMAGE = "assets/bg.jpg"
OBS_SPAWN_INTERVAL = 200
ENEMY_INTERVAL = 150
OBS_INTERVAL = 50
REGEN_INTERVAL = 400
OBSTACLE_DAMAGE = 9
POWER_UP_INTERVAL = 100
ENEMY_BULLET_HEIGHT = 7
ENEMY_BULLET_WIDTH = 9
ENEMY_BULLET_SPEED = 7
SCORES = "scores.csv"
INFO = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = INFO.current_w, INFO.current_h
SPREAD_INTERVAL = 750
pygame.font.init()
FONT = pygame.font.Font(FONT_PATH, 36)
POWER_UP_TYPES = ["heal","spread"]
PLAYER_SPEED = 10

OBSTACLE_SIZE = 25
ASTEROID_PATH = "assets/asteroid.png"

HEALTH = pygame.transform.scale(pygame.image.load("assets/healthpack.png"),(30,30))
BULLET = pygame.transform.scale(pygame.image.load("assets/bulletpack.png"),(20,30))
img = pygame.image.load("assets/gameover.png")
GAME_OVER_IMAGE = pygame.transform.scale(img,(SCREEN_WIDTH,SCREEN_HEIGHT))

START_BG = pygame.transform.scale(pygame.image.load("assets/start.png"),(SCREEN_WIDTH,SCREEN_HEIGHT))

ENEMY_PATH = "assets/enemyship.png"