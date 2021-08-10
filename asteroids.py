import pygame
import math
import numpy as np
from random import sample
import Agent as A
import Enemy as E
import Bullet as B
import helper as H


class AsteroidsAI(object):
    """ """
    
    def __init__(self):
        """ Attributes of game object. """
        self.shoot_count = 0
        self.time_count = 0
        self.score = 0
        self.game_ended = False
        # Setup sprite groups for use in collision detection
        self.objects = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # Instantiate agent object
        self.agent = A.Agent()
        self.objects.add(self.agent)
    
    def calculate_frame(self):
        """ Main game loop of an agent. """
        # Get keys for input checks
        keys = pygame.key.get_pressed()

        # Shooting only possible three times per second
        if self.shoot_count >= H.FPS//3:
            # Shoot on 'space'
            if keys[pygame.K_SPACE]:
                # Spawn bullet from agent and add to sprite groups for collision
                bullet = B.Bullet(self.agent)
                self.objects.add(bullet)
                self.bullets.add(bullet)
                self.shoot_count = 0

        # Spawn enemies with random size every 3 seconds
        if self.time_count >= H.FPS*3:
            scale = sample([50, 100, 150], k=1)[0]
            enemy = E.Enemy(scale)
            self.objects.add(enemy)
            self.enemies.add(enemy)
            self.time_count = 0

        # Collision detection for death (agent,enemy) and score (bullet,enemy)
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.agent, enemy):
                enemy.kill()
                # destroy every object
                for obj in self.enemies:
                    obj.kill()
                self.game_ended = True
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(bullet, enemy):
                    self.score += 10
                    bullet.kill()
                    # If an enemy is shot, spawn two new, smaller enemies
                    if enemy.scale == 150:
                        e1 = E.Enemy(100)
                        e2 = E.Enemy(100)
                        e1.pos_x, e1.pos_y = enemy.pos_x, enemy.pos_y
                        e2.pos_x, e2.pos_y = enemy.pos_x+50, enemy.pos_y+50
                        self.enemies.add(e1)
                        self.enemies.add(e2)
                        self.objects.add(e1)
                        self.objects.add(e2)
                        enemy.kill()
                    elif enemy.scale == 100:
                        e1 = E.Enemy(50)
                        e2 = E.Enemy(50)
                        e1.pos_x, e1.pos_y = enemy.pos_x, enemy.pos_y
                        e2.pos_x, e2.pos_y = enemy.pos_x+25, enemy.pos_y+25
                        self.enemies.add(e1)
                        self.enemies.add(e2)
                        self.objects.add(e1)
                        self.objects.add(e2)
                        enemy.kill()
                    else:
                        enemy.kill()
                        self.score += 40

        # If game is over, wait for agent to restart or quit the game
        if self.game_ended:
            # Draw background and gameover display
            #BLTscreen.blit(bg, (0, 0))
            display = "GAME OVER! Your score is " + str(self.score) + "."
            gameover_display = H.font_over.render(display, True, (255,255,255))
            """BLTscreen.blit(gameover_display, (H.WIDTH/2 - gameover_display.get_width()/2, 
                                           H.HEIGHT/2 - gameover_display.get_height()/2))
            BLTscreen.blit(H.again_display, (H.WIDTH/2 - H.again_display.get_width()/2, 
                                        H.HEIGHT/2 - H.again_display.get_height()/2 
                                        + gameover_display.get_height()))"""
            # Restart on 'r'
            if keys[pygame.K_r]:
                self.score = 0
                self.agent.pos_x, self.agent.pos_y = H.WIDTH//2, H.HEIGHT//2
                self.agent.rect = self.agent.img.get_rect(center=(self.agent.pos_x, self.agent.pos_y))
                #BLTscreen.blit(self.agent.img, self.agent.rect)
                self.game_ended = False
        else:
            # Draw background image onto screen at top left corner
            #BLTscreen.blit(bg, (0, 0))
            self.score_display = H.font_score.render(str(self.score), True, (255,255,255))

            # Update objects and draw on screen
            for obj in self.objects:
                obj.move()
                #BLTscreen.blit(obj.img, obj.rect)

            # get observations
            #get_obs(self.agent, self.enemies)

            # Draw score onto screen
            #BLTscreen.blit(score_display, (10, 10))

        # Increase time vars every update
        #clock.tick(H.FPS)
        self.time_count += 1
        self.shoot_count += 1

        # Update display every frame; to-do: only update one agent's screen
        pygame.display.update()
    
    def get_obs(self, agent, asteroids):
        """ Get agent observations (angle of the agent and distances to asteroids) as inputs for the NN. """
        angle = agent.angle
        distances = []
        asteroids = list(asteroids)

        # calculate distance to agent for each asteroid
        for a in asteroids:
            distance = math.sqrt((a.rect.center[0] - agent.direction[0])**2 + (a.rect.center[1] - agent.direction[1])**2) # falls nicht, dann einzeln
            distances.append(distance)

        if len(distances) == 0:
            return angle

        # if distances list is not empty, get mininmum distance and corresponding asteroid
        min_distance = min(distances)
        min_idx = distances.index(min_distance)
        a = asteroids[min_idx]

        # get two vectors and calculate angle between spaceship and closest asteroid
        u_x = agent.direction[0] - agent.rect.center[0]
        u_y = agent.direction[1] - agent.rect.center[1]
        v_x = a.rect.center[0] - agent.direction[0]
        v_y = a.rect.center[1] - agent.direction[1]

        closest_angle = math.degrees(math.acos(np.dot(np.array([u_x, u_y]), np.array([v_x, v_y]))
                                             / np.dot(np.linalg.norm(np.array([u_x, u_y])), np.linalg.norm(np.array([v_x, v_y])))))

        # return inputs for NN
        return angle, min_distance, closest_angle
    
    def display(self, blit = False):
        if blit == True:
            screen.blit(bg, (0, 0))
            for obj in self.objects:
                    screen.blit(obj.img, obj.rect)
            
            screen.blit(self.score_display, (10, 10))

# Main guard prevents running on import
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    
    # Fix FPS
    clock = pygame.time.Clock()

    # Create game window screen
    screen = pygame.display.set_mode((H.WIDTH, H.HEIGHT))
    
    # Game title
    pygame.display.set_caption("Asteroids")
    # Asteroid icon: https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
    img = pygame.image.load("images/meteorite.png")
    pygame.display.set_icon(img)
    # Background: https://wallpapertag.com/wallpaper/full/a/5/b/547899-large-star-sky-wallpaper-3100x1740-4k.jpg
    bg = pygame.image.load("images/star_sky.jpg")
    bg = pygame.transform.scale(bg, (H.WIDTH, H.HEIGHT))
    
    # instantiate multiple agents/games
    game_list = []
    for _ in range(H.N_AGENTS):
        game = AsteroidsAI()
        game_list.append(game)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for game in game_list:
            game.calculate_frame()
        if len(game_list) > 0:
            if game_list[0].game_ended == True:
                game_list.pop(0)
            else:
                game_list[0].display(True)
        else:
            break
    # Quit the game after application is not 'running' anymore
    pygame.quit()

