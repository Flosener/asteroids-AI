import pygame
import math
import numpy as np
from random import sample
import Player as P
import Enemy as E
import Bullet as B
import helper as H


class Environment(object):
    """ The main game loop for getting observations and displaying the training. """
    
    def __init__(self):
        """ Attributes of game object. """
        self.shoot_count = 0
        self.time_count = 0
        self.frames = 0
        self.score = 0
        self.game_ended = False
        # Setup sprite groups for use in collision detection
        self.objects = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # Instantiate player object
        self.player = P.Player()
        self.objects.add(self.player)
    
    def calculate_frame(self, action):
        """ Main game loop. """
        # Get keys for input checks
        keys = pygame.key.get_pressed()

        # Shooting only possible three times per second
        if self.shoot_count >= H.FPS//3:
            if action[0] > 0:
                # Spawn bullet from player and add to sprite groups for collision
                bullet = B.Bullet(self.player)
                self.objects.add(bullet)
                self.bullets.add(bullet)
                self.shoot_count = 0

        # Spawn enemies with random size every 3 seconds
        if self.time_count >= H.FPS*1:
            scale = sample([50, 100, 150], k=1)[0]
            enemy = E.Enemy(scale)
            self.objects.add(enemy)
            self.enemies.add(enemy)
            self.time_count = 0

        # Collision detection for death (player,enemy) and score (bullet,enemy)
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
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

        # If game is over, wait for player to restart or quit the game
        if self.game_ended:
            # Restart on 'r'
            if keys[pygame.K_r]:
                self.score = 0
                self.player.pos_x, self.player.pos_y = H.WIDTH//2, H.HEIGHT//2
                self.player.rect = self.player.img.get_rect(center=(self.player.pos_x, self.player.pos_y))
                #BLTscreen.blit(self.player.img, self.player.rect)
                self.game_ended = False
        else:
            # Draw background image onto screen at top left corner
            self.score_display = H.font_score.render(str(self.score), True, (255,255,255))

            # Update objects and draw on screen
            for obj in self.objects:
                if type(obj) == type(self.player):
                    obj.move(action[1], action[2])
                else: obj.move()

        # Increase time vars every update
        self.time_count += 1
        self.shoot_count += 1
        self.frames += 1

        # Update display every frame; to-do: only update one player's screen
        pygame.display.update()
        
        print(type(self.get_obs(self.player, self.enemies)))
        return self.get_obs(self.player, self.enemies)
    
    
    def get_obs(self, player, asteroids):
        """ Get player observations (angle of the player and distances to asteroids) as inputs for the NN. """
        angle = player.angle
        distances = []
        asteroids = list(asteroids)

        # calculate distance to player for each asteroid
        for a in asteroids:
            distance = math.sqrt((a.rect.center[0] - player.direction[0])**2 + (a.rect.center[1] - player.direction[1])**2) # falls nicht, dann einzeln
            distances.append(distance)

        if len(distances) == 0:
            return angle

        # if distances list is not empty, get mininmum distance and corresponding asteroid
        min_distance = min(distances)
        min_idx = distances.index(min_distance)
        a = asteroids[min_idx]

        # get two vectors and calculate angle between spaceship and closest asteroid
        u_x = player.direction[0] - player.rect.center[0]
        u_y = player.direction[1] - player.rect.center[1]
        v_x = a.rect.center[0] - player.direction[0]
        v_y = a.rect.center[1] - player.direction[1]

        closest_angle = math.degrees(math.acos(np.dot(np.array([u_x, u_y]), np.array([v_x, v_y]))
                                             / np.dot(np.linalg.norm(np.array([u_x, u_y])), np.linalg.norm(np.array([v_x, v_y])))))

        # return inputs for NN
        return np.array([angle, min_distance, closest_angle], dtype=np.float32)
    
    
    def display(self, blit=False):
        """ Display the game objects. """
        if blit == True:
            H.screen.blit(H.bg, (0, 0))
            for obj in self.objects:
                    H.screen.blit(obj.img, obj.rect)
            H.screen.blit(self.score_display, (10, 10))