import pygame
import random
import enemy
import obstacle
from particle import Particle
import powerup
from constants import *
import sys



class SpaceInvaders:

    __slots__ = ["screen","enemies","damage_multiplier","bullets","player","particles","player_health","max_health","health_bar_length","health_ratio","player_speed","player_damage","multiplier","bg","min","max","player_image","last_shot_time","shooting_delay","is_spread_active","spread_duration","spread_activated_time","powerups","obstacles","score"]


    def __init__(self):
        pygame.init()
        self.score = 0
        self.min = 100
        self.max = 350
        self.bg = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Space Trivia Invaders")
        self.enemies = [enemy.Enemy(self.min,self.max) for _ in range(random.randint(5,10))]
        player_image_original = pygame.image.load(PLAYER_IMAGE)
        self.player_image = pygame.transform.scale(player_image_original, (PLAYER_SIZE, PLAYER_SIZE))
        self.player = self.player_image.get_rect()
        self.player.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.player.topleft = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60
        self.player.width = PLAYER_SIZE
        self.player.height = PLAYER_SIZE
        self.bullets = []
        self.powerups = []
        self.obstacles = []
        self.particles = []
        self.player_speed = 10 
        self.player_damage = 8
        self.multiplier = 1
        self.last_shot_time = 0
        self.shooting_delay = 50
        self.is_spread_active = False
        self.spread_duration = 7000
        self.spread_activated_time = 0
        self.player_health = 100  # Example starting health
        self.max_health = 100     # Maximum health
        self.health_bar_length = 200  # Total length of the health bar
        self.health_ratio = self.health_bar_length / self.max_health
        self.damage_multiplier = 1

    def mainloop(self):
        clock = pygame.time.Clock()
        enemy_move_timer = 0
        spread_timer = 0
        enemy_timer = 0
        obstacle_move_timer = 0
        obstacle_spawn_timer = 0
        power_up_timer = 0
        enemy_bullets = []
        running = True
        while running:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.player_speed /= 2
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.player_speed *= 2

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time >= self.shooting_delay:
                    if self.is_spread_active:
                        # Create spread bullets
                        self.bullets.append(pygame.Rect(self.player.centerx, self.player.y, BULLET_SIZE, BULLET_SIZE))  # Central bullet
                        self.bullets.append(pygame.Rect(self.player.centerx - 10, self.player.y, BULLET_SIZE, BULLET_SIZE))  # Left bullet
                        self.bullets.append(pygame.Rect(self.player.centerx + 10, self.player.y, BULLET_SIZE, BULLET_SIZE))  # Right bullet
                        self.bullets.append(pygame.Rect(self.player.centerx - 20, self.player.y, BULLET_SIZE, BULLET_SIZE))  # Left bullet
                        self.bullets.append(pygame.Rect(self.player.centerx + 20, self.player.y, BULLET_SIZE, BULLET_SIZE))  # Right bullet
                    else:
                        # Create a normal bullet
                        self.bullets.append(pygame.Rect(self.player.centerx, self.player.y, BULLET_SIZE, BULLET_SIZE))
                    self.last_shot_time = current_time
            if keys[pygame.K_a] and self.player.x > 0:
                self.player.x -= self.player_speed
            if keys[pygame.K_d] and self.player.x < SCREEN_WIDTH - self.player.width:
                self.player.x += self.player_speed

            # For moving up (W key), check if the player's y position is greater than 0
            if keys[pygame.K_w] and self.player.y > 0:
                self.player.y -= self.player_speed

            # For moving down (S key), check if the player's y position is less than the screen height minus the player's height
            if keys[pygame.K_s] and self.player.y < SCREEN_HEIGHT - self.player.height:
                self.player.y += self.player_speed

            # For resetting the position (R key), center the player on the screen
            if keys[pygame.K_r]:
                self.player.x = SCREEN_WIDTH // 2 - self.player.width // 2  # Center horizontally
                self.player.y = SCREEN_HEIGHT // 2 - self.player.height // 2  # Center vertically

            if keys[pygame.K_ESCAPE]:
                pygame.QUIT
                sys.exit()

            for bullet in self.bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.y < 0:
                    self.bullets.remove(bullet)

            enemy_move_timer += dt
            obstacle_spawn_timer += dt
            obstacle_move_timer += dt
            enemy_timer += dt
            power_up_timer += dt
            if self.is_spread_active:
                spread_timer += dt // 4
            if enemy_move_timer >= ENEMY_INTERVAL:
                for enemy in self.enemies:
                    enemy.move(ENEMY_SPEED)  # Move each enemy
                if enemy.y() > SCREEN_HEIGHT:
                    running = False  # Game over
                enemy_move_timer = 0  # Reset the timer

            if obstacle_move_timer >= OBS_INTERVAL:
                for obstacle in self.obstacles:
                    obstacle.move()
                obstacle_move_timer = 0

            if obstacle_spawn_timer >= OBS_SPAWN_INTERVAL and self.should_obstacle_spawn():
                self.spawn_obstacle()
                obstacle_spawn_timer = 0  # Reset the timer

            if enemy_timer >= ENEMY_INTERVAL and self.should_enemy_spawn():
                self.spawn_enemy(self.enemies)
                enemy_timer = 0  # Reset the timer

            if power_up_timer >= POWER_UP_INTERVAL and self.should_power_up_spawn():
                self.spawn_power_up(self.powerups)
                power_up_timer = 0

            if self.is_spread_active and spread_timer > SPREAD_INTERVAL:
                self.is_spread_active = False
                spread_timer = 0

            for bullet in self.bullets[:]:
                for enemy in self.enemies[:]:
                    if bullet.colliderect(enemy.get_rect()):
                        if enemy.get_hp() <= (self.player_damage * self.multiplier):
                            self.enemies.remove(enemy)
                            self.score += 50
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                        else:
                            enemy.reduce_hp(self.player_damage*self.multiplier)
                if self.should_enemy_shoot(enemy_bullets):
                    enemy = self.enemies[random.randrange(0,len(self.enemies))]
                    enemy_bullets.append(enemy.shoot())


            for particle in self.particles[:]:
                particle.move()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)

            # Move enemy bullets
            for bullet in enemy_bullets:
                bullet.move()
                if bullet.rect.y > SCREEN_HEIGHT:
                    enemy_bullets.remove(bullet)
            
            for powerup in self.powerups:
                powerup.move()

            # Draw everything

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.player_image, self.player.topleft)

            for bullet in self.bullets:
                pygame.draw.rect(self.screen, GREEN, bullet)

            for enemy in self.enemies:
                enemy.draw(self.screen)
                if(enemy.get_rect().colliderect(self.player)) or (enemy.get_rect().y >= SCREEN_HEIGHT):
                    show_end_screen(self.screen,self.score)

            for bullet in enemy_bullets:
                bullet.draw(self.screen)


            for powerup in self.powerups:
                powerup.draw(self.screen)

                if self.player.colliderect(powerup.rect):  # Check for collision
                    self.activate_powerup(powerup.type)
                    self.powerups.remove(powerup)
            
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
                if self.player.colliderect(obstacle.rect):  # Check for collision
                    self.player_health -= OBSTACLE_DAMAGE * self.damage_multiplier
                    if self.score > 0:
                        self.score -= 15
                    self.obstacles.remove(obstacle)
                
            for bullet in enemy_bullets:
                bullet.draw(self.screen)
                if bullet.collide_rect(self.player) or bullet.rect.y > SCREEN_HEIGHT:
                    self.player_health -= self.damage_multiplier 
                    enemy_bullets.remove(bullet)
                    if self.player_health <= 0:
                        show_end_screen(self.screen,self.score)

            for particle in self.particles:
                particle.draw(self.screen) 

            
            self.draw_health_bar(self.player_health)
            self.display_score(self.score)

            pygame.display.flip()  
            pygame.time.delay(10)

    def should_obstacle_spawn(self):
        return random.randint(0,100) < 10

    def activate_powerup(self, powerup_type):
        if powerup_type == "spread":
            # Activate spread shot power-up
            self.create_particles(self.player.x,self.player.y,(0,0,255))
            self.is_spread_active = True
            self.spread_activated_time = pygame.time.get_ticks()
        if powerup_type == "heal":
            self.create_particles(self.player.x,self.player.y,(0,255,0))
            self.player_health += 15
            

    def create_particles(self, x, y,color, num_particles=50):
        for _ in range(num_particles):
            self.particles.append(Particle(x, y,color))

    def should_enemy_shoot(self,enemy_bullets):
        if len(enemy_bullets) < 30:
            return random.randint(0, 100) < 1  # 1% chance for each enemy to shoot each frameaa

    def draw_health_bar(self, current_health):
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, self.health_bar_length, 20))
        current_health_length = current_health * self.health_ratio
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, current_health_length, 20))

    def spawn_obstacle(self):
        new_obstacle = obstacle.Obstacle(15)
        self.obstacles.append(new_obstacle)

    def spawn_enemy(self,enemies):
        new_enemy = enemy.Enemy(self.min,self.max)
        enemies.append(new_enemy)

    def spawn_power_up(self,power_ups):
        rand_index = random.randrange(0, len(POWER_UP_TYPES))
        rand_type = POWER_UP_TYPES[rand_index]
        new_power_up = powerup.PowerUp(random.randint(0,SCREEN_WIDTH),random.randint(0,100),5,5,rand_type)
        power_ups.append(new_power_up)

    def should_power_up_spawn(self):
        if len(self.powerups) < 10 and (random.randint(0,100) < 0.05):
            return True
        return False

    def should_enemy_spawn(self):
        if len(self.enemies) < 15 and (random.randint(0,100) < 10):
            return True
        return False
    
    def display_score(self, score):
        score_text = FONT.render(f'Score: {score}', True, (255, 255, 255))  # White color
        self.screen.blit(score_text, (10, 40))  # Position the score at the top-left corner
        
def show_start_screen(screen):
    running = True
    title_font = pygame.font.Font(None, 80)  # Large font for the title
    prompt_font = pygame.font.Font(None, 40)  # Smaller font for the prompt

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False  # Return False if the window is closed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game on pressing Enter
                    running = False
                    return True

        screen.fill((0, 0, 0))  # Fill the screen with black or any other color

        # Render the title
        title_surface = title_font.render('Space Invaders', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        screen.blit(title_surface, title_rect)

        # Render the start prompt
        prompt_surface = prompt_font.render('Press Enter to Start', True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3))
        screen.blit(prompt_surface, prompt_rect)

        pygame.display.flip()  # Update the display

    return True  # Return True if the game should start

def show_end_screen(screen, score):
    restart = False
    running = True
    title_font = pygame.font.Font(None, 80)
    prompt_font = pygame.font.Font(None, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    restart = True
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))

        title_surface = title_font.render('Game Over!', True, (255, 255, 255))
        score_surface = prompt_font.render('Score: ' + str(score), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        prompt_surface = prompt_font.render('Press Enter to Restart or Escape key to exit', True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3))

        screen.blit(title_surface, title_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(prompt_surface, prompt_rect)

        pygame.display.flip()

    if restart:
        # Restart the game
        game = SpaceInvaders()
        game.mainloop()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    if(show_start_screen(screen)):
        game = SpaceInvaders()
        game.mainloop()
    else:
        pygame.quit()
    

