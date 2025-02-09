import csv
import math
import os
import pygame
import random
import enemy
from fire import Flame
import obstacle
from particle import Particle
import powerup
from constants import *
import sys

NEGATIVE = pygame.transform.scale(pygame.image.load(NEGATIVE_IMAGE), (PLAYER_SIZE, PLAYER_SIZE))
NORMAL = pygame.transform.scale(pygame.image.load(PLAYER_IMAGE), (PLAYER_SIZE, PLAYER_SIZE))


class SpaceInvaders:

    __slots__ = ["enemy_speed","regen_activated_time","regen","dead_zone","control","joystick","screen","enemies","damage_multiplier","bullets","player","player_pos","particles","player_health","max_health","health_bar_length","health_ratio","player_speed","player_damage","multiplier","bg","min","max","player_image","last_shot_time","shooting_delay","is_spread_active","spread_duration","spread_activated_time","powerups","obstacles","score"]


    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load("assets/icon.jpg"))
        player_image_original = pygame.image.load(PLAYER_IMAGE)
        self.player_image = pygame.transform.scale(player_image_original, (PLAYER_SIZE, PLAYER_SIZE))
        self.player = self.player_image.get_rect()
        self.score = 0
        self.min = 100
        self.max = 350
        self.regen = False
        self.bg = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.enemies = [enemy.Enemy(self.min,self.max, self.player.x) for _ in range(random.randint(5,10))]
        self.player.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.player.topleft = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60
        self.player.width = PLAYER_SIZE
        self.player.height = PLAYER_SIZE
        self.bullets = []
        self.powerups = []
        self.obstacles = []
        self.particles = []
        self.player_damage = 2.5
        self.multiplier = 1
        self.last_shot_time = 0
        self.shooting_delay = 50
        self.is_spread_active = False
        self.spread_duration = 7000
        self.spread_activated_time = 0
        self.player_health = 100 
        self.max_health = 100     # Maximum health
        self.health_bar_length = 200  # Total length of the health bar
        self.health_ratio = self.health_bar_length / self.max_health
        self.damage_multiplier = 1
        if pygame.joystick.get_count() == 0:
            self.control = "keyboard"
            self.joystick = None
            self.player_speed = PLAYER_SPEED
        else:
            self.dead_zone = 0.1
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.player_pos = [SCREEN_WIDTH//2,SCREEN_HEIGHT]
            self.control = "joystick"
            self.player_speed = 5
        self.enemy_speed = ENEMY_SPEED

    def mainloop(self):
        clock = pygame.time.Clock()
        enemy_move_timer = 0
        spread_timer = 0
        enemy_timer = 0
        regen_timer = 0
        obstacle_move_timer = 0
        obstacle_spawn_timer = 0
        power_up_timer = 0
        enemy_bullets = []
        running = True
        pressing = False

        while running:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            pygame.quit
                            sys.exit()
                if self.control == "keyboard":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                            self.player_speed /= 2
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                            self.player_speed *= 2
                    
                if self.control == "joystick":
                    if event.type == pygame.JOYBUTTONDOWN or pressing:
                        if self.joystick.get_button(0):
                            pressing = True
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
                        if self.joystick.get_button(5):
                            self.player_speed /= 2

                    if event.type == pygame.JOYAXISMOTION:
                                self.player_pos[0] = self.joystick.get_axis(0) # Left thumbstick horizontal
                                self.player_pos[1] = self.joystick.get_axis(1)  # Left thumbstick vertical

                                if abs(self.player_pos[0]) < self.dead_zone:
                                    self.player_pos[0] = 0
                                if abs(self.player_pos[1]) < self.dead_zone:
                                    self.player_pos[1] = 0

                                # Update player position
                                if(self.player_pos[0] < SCREEN_WIDTH and self.player_pos[1] < SCREEN_HEIGHT):
                                    self.player.x += self.player_pos[0] * self.player_speed
                                    self.player.y += self.player_pos[1] * self.player_speed
                    

                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 5:
                            self.player_speed *= 2
                        # if event.button == 0:
                        #     pressing = False

                        

            if self.control == "keyboard":
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

            if self.regen:
                regen_timer += dt // 3.5
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

            if regen_timer >= REGEN_INTERVAL:
                self.regen = False
                regen_timer = 0
            

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
                    if is_enemy_in_line_of_sight(self.player,enemy):
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

                if powerup.get_rect().y >= SCREEN_HEIGHT:
                    self.powerups.remove(powerup)

            # Draw everything

            self.screen.blit(self.bg, (0, 0))
            if self.is_spread_active:
                self.player_speed = 15
                if power_up_timer > 0 and power_up_timer % 10 == 0:
                    self.player_image = NEGATIVE
                else:
                    self.player_image = NORMAL
                
            else:
                self.player_image = NORMAL
                self.player_speed = 10

            self.screen.blit(self.player_image, self.player.topleft)

            for bullet in self.bullets:
                color = (0,255,0)
                if self.is_spread_active:
                    if power_up_timer > 0 and power_up_timer % 5 == 0:
                        color = (255,255,255)
                    else:
                        color = (0,255,0)
                    
                else:
                    color = (0,255,0)
                pygame.draw.rect(self.screen,color , bullet)


            for enemy in self.enemies:
                enemy.draw(self.screen)
                if not self.is_spread_active and (enemy.get_rect().colliderect(self.player)) or (enemy.get_rect().y >= SCREEN_HEIGHT):
                    show_end_screen(self.screen,self.score)

            for powerup in self.powerups:
                powerup.draw(self.screen)
                if powerup.collide(self.player):  # Check for collision
                    self.activate_powerup(powerup.type)
                    power_up_timer = 0
                    self.powerups.remove(powerup)
            
            for obstacle in self.obstacles:
                self.create_flames(obstacle.get_rect().x + 10,obstacle.get_rect().y + 10,5)
                obstacle.draw(self.screen)
                if not self.is_spread_active and self.player.colliderect(obstacle.rect):  # Check for collision
                    self.player_health -= OBSTACLE_DAMAGE * self.damage_multiplier
                    if self.score > 0:
                        self.score -= 15
                    self.obstacles.remove(obstacle)
                    self.shake_screen(2,5)
                if obstacle.get_rect().y > SCREEN_HEIGHT:
                    self.obstacles.remove(obstacle)
                
            for bullet in enemy_bullets:
                bullet.draw(self.screen)
                if bullet.collide_rect(self.player) or bullet.rect.y > SCREEN_HEIGHT:
                    self.player_health -= self.damage_multiplier 
                    enemy_bullets.remove(bullet)
                    if self.player_health <= 0:
                        show_end_screen(self.screen,self.score)
                if bullet.get_y() > SCREEN_HEIGHT:
                    enemy_bullets.remove(bullet)

            for particle in self.particles:
                particle.draw(self.screen) 

            if dt % 5 == 0 and self.regen and self.player_health < 94.5:
                self.player_health += 5.5
            
            
            self.draw_health_bar(self.player_health)
            self.display_score(self.score)

            pygame.display.flip()  
            pygame.time.delay(10)

    def should_obstacle_spawn(self):
        return random.randint(0,100) < 10
    
    
    def shake_screen(self, duration, intensity):
        original_pos = self.screen.get_rect().topleft
        elapsed = 0
        clock = pygame.time.Clock()

        while elapsed < duration:
            dx, dy = random.randint(-intensity, intensity), random.randint(-intensity, intensity)
            screen_scroll = original_pos[0] + dx, original_pos[1] + dy
            screen.blit(self.screen, screen_scroll) # Redraw background at the offset position

            pygame.display.flip()
            elapsed += clock.tick(60)

        # Reset the screen to its original position
        screen.blit(self.screen, original_pos)
        pygame.display.flip()


    def activate_powerup(self, powerup_type):
        if powerup_type == "spread":
            # Activate spread shot power-up
            self.create_particles(self.player.x,self.player.y,(0,0,255))
            self.is_spread_active = True
            self.spread_activated_time = pygame.time.get_ticks()
        if powerup_type == "heal":
            self.create_particles(self.player.x,self.player.y,(255,255,0))
            self.player_health += 15
            self.regen = True
            self.regen_activated_time = pygame.time.get_ticks()
            

    def create_particles(self, x, y,color, num_particles=50):
        for _ in range(num_particles):
            self.particles.append(Particle(x, y,color))

    def create_flames(self, x, y, num_particles=50):
        for _ in range(num_particles):
            self.particles.append(Flame(x, y))

    def should_enemy_shoot(self,enemy_bullets):
        if len(enemy_bullets) < 30:
            return random.randint(0, 100) < 1  # 1% chance for each enemy to shoot each frame

    def draw_health_bar(self, current_health):
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, self.health_bar_length, 20))
        current_health_length = current_health * self.health_ratio
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, current_health_length, 20))

    def spawn_obstacle(self):
        new_obstacle = obstacle.Obstacle(15)
        self.obstacles.append(new_obstacle)

    def spawn_enemy(self,enemies):
        new_enemy = enemy.Enemy(self.min,self.max,self.player.x)
        enemies.append(new_enemy)

    def spawn_power_up(self,power_ups):
        rand_index = random.randrange(0, len(POWER_UP_TYPES))
        rand_type = POWER_UP_TYPES[rand_index]
        new_power_up = powerup.PowerUp(random.randint(0,SCREEN_WIDTH),random.randint(0,100),rand_type)
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
        

def is_enemy_in_line_of_sight(player, enemy):
    distance = math.sqrt((enemy.get_rect().x - player.x) ** 2 + (enemy.get_rect().y - player.y) ** 2)
    return distance <= SCREEN_HEIGHT

def get_input(prompt,score):
    text = ''
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        screen.fill((0,0,0),pygame.rect.Rect(0,0,SCREEN_WIDTH,SCREEN_WIDTH))
        title_surf = FONT.render("New high score!",True,(0,255,255))
        text_surface = FONT.render(prompt+ text, True, (0,255,255))
        screen.blit(title_surf,(SCREEN_WIDTH //2 - title_surf.get_width(),30))
        screen.blit(text_surface, (SCREEN_WIDTH/2 - text_surface.get_width(), SCREEN_HEIGHT/2 - text_surface.get_height()))
        pygame.display.flip()

    save_score(text,score,SCORES)
    display_high_scores(screen)


def save_score(player_name, player_score, file_name):
    fieldnames = ['name', 'score']
    file_exists = os.path.isfile(file_name)  # Check if file already exists


    with open(file_name, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:  # If the file does not exist, write the header
            writer.writeheader()

        writer.writerow({'name': player_name, 'score': player_score})

def show_start_screen(screen):
    message = 'Press Enter to Start (Press H to learn how to play or ESC to exit)'
    elapsed_time = 0
    running = True
    current_color = FONT_COLORS[random.randint(0,len(FONT_COLORS) - 1)]

    timer = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False  # Return False if the window is closed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game on pressing Enter
                    running = False
                    game = SpaceInvaders()
                    game.mainloop()
                if event.key == pygame.K_h:  # Press 'H' to open How to Play screen
                    show_how_to_play_screen(screen)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    display_high_scores(screen)
                

        screen.blit(START_BG,(0,0))

        # Render the title


        if elapsed_time % 7 == 0:
            current_color = FONT_COLORS[0]
        else:
            current_color = FONT_COLORS[1]
        

        # Render the start prompt
        prompt_surface = render_text(message,current_color,35)
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3))
        screen.blit(prompt_surface, prompt_rect)

        prompt_surface2 = render_text("You can also press S to view the high scores",current_color,35)
        prompt_rect2 = prompt_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 2.7))
        screen.blit(prompt_surface2, prompt_rect2)


        pygame.display.flip()  # Update the display

        time = timer.tick(60)
        elapsed_time += time

    return True  # Return True if the game should start

def display_high_scores(screen, scores_file=SCORES):
    # Read scores from file
    with open(scores_file, 'r') as file:
        reader = csv.DictReader(file)
        scores = [row for row in reader]


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    show_start_screen(screen)  # Ensure this function is defined

        bg = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE), (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bg, (0, 0))

        title_surf = FONT.render("High Scores", True, (0, 255, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surf, title_rect)

        start_y = 100
        if scores:
            for score in scores:
                score_surf = FONT.render(f"{score['name']} - {score['score']}", True, (0, 255, 0))
                score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y))
                screen.blit(score_surf, score_rect)
                start_y += 50
        else:
            no_scores_surf = FONT.render("No high scores yet", True, (100, 0, 0))
            no_scores_rect = no_scores_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y))
            screen.blit(no_scores_surf, no_scores_rect)

        prompt_surf = FONT.render("Press ENTER to return to start screen or ESC to exit", True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(prompt_surf, prompt_rect)

        pygame.display.flip()  # Update the display


def render_text(message,color,size):

    font = pygame.font.Font(FONT_PATH,size)
    return font.render(message,True,color,(0,0,0))

def show_how_to_play_screen(screen):
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Return from the function if the window is closed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Return to main menu on pressing Enter
                    running = False

        screen.fill((0, 0, 0))  # Fill the screen with black or any other color

        # Render the instructions
        instructions = [
            "How to Play:",
            "Move the spaceship using WASD keys.",
            "Shoot using the Spacebar.",
            "Pick up power-ups for extra abilities.",
            "Yellow balls heal you and blue balls give you bullet spread",
            "Hold Shift to slow down your ship.",
            "",
            "Press Enter to return to the main menu."
        ]

        for i, line in enumerate(instructions):
            text_surface = render_text(line, (255, 255, 255),25)
            screen.blit(text_surface, (50, 30 + 30 * i))

        pygame.display.flip()  # Update the display

def show_end_screen(screen, player_score):
    timer = pygame.time.Clock()
    elapsed_time = 0
    restart = False
    running = True

    # Read the existing high scores
    with open(SCORES, 'r') as f:
        reader = csv.DictReader(f)
        scores = [row for row in reader]
        scores.sort(key=lambda x: int(x['score']), reverse=True)


    new_high_score = False
    if not scores or int(scores[0]['score']) < player_score:
        new_high_score = True

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

        score_surface = render_text('Score: ' + str(player_score), (255, 255, 255),45)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        if new_high_score and elapsed_time > 3000:
            get_input("Enter your name: ", player_score)
        
        prompt_surface = render_text('Press Enter to Restart or Escape key to exit', (255, 255, 255),45)
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3 - 30))
        screen.blit(GAME_OVER_IMAGE,(0,0))
        screen.blit(score_surface, score_rect)
        if not new_high_score:
            screen.blit(prompt_surface, prompt_rect)

        pygame.display.flip()
        time = timer.tick(60)
        elapsed_time += time

    if restart:
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
    

