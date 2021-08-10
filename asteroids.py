import pygame
import math
import numpy as np
from random import sample
import Agent as A
import Enemy as E
import Bullet as B

# Global variables
WIDTH = 1200
HEIGHT = 700


# TO DO:
# reset after death of whole population
# step(action) -> direction
# game_iteration (keep track of frames)
# display one agent after another

def get_obs(agent, asteroids):
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
    
    return angle, min_distance, closest_angle
    

def main():
    """ The main function of our asteroids game. """
    
    # Initialize pygame
    pygame.init()
    
    # Fix FPS
    clock = pygame.time.Clock()
    FPS = 60
    
    # Gameloop variables
    shoot_count = 0
    time_count = 0
    score = 0
    game_ended = False

    # Create game window screen
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    
    # Game title
    pygame.display.set_caption("Asteroids")
    # Asteroid icon: https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
    img = pygame.image.load("images/meteorite.png")
    pygame.display.set_icon(img)
    # Background: https://wallpapertag.com/wallpaper/full/a/5/b/547899-large-star-sky-wallpaper-3100x1740-4k.jpg
    bg = pygame.image.load("images/star_sky.jpg")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    
    # Score display
    font_over = pygame.font.SysFont("Georgia", 60)
    font_score = pygame.font.SysFont("Georgia", 30)
    again_display = font_score.render("Press 'r' to restart.", True, (255,255,255))
    
    # Setup sprite groups for use in collision detection
    objects = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    # Instantiate agent object
    agent = A.Agent()
    objects.add(agent)
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get keys for input checks
        keys = pygame.key.get_pressed()
        
        # Shooting only possible three times per second
        if shoot_count >= FPS//3:
            # Shoot on 'space'
            if keys[pygame.K_SPACE]:
                # Spawn bullet from agent and add to sprite groups for collision
                bullet = B.Bullet(agent)
                objects.add(bullet)
                bullets.add(bullet)
                shoot_count = 0
        
        # Spawn enemies with random size every 3 seconds
        if time_count >= FPS*20:
            scale = sample([50, 100, 150], k=1)[0]
            enemy = E.Enemy(scale)
            objects.add(enemy)
            enemies.add(enemy)
            time_count = 0

        # Collision detection for death (agent,enemy) and score (bullet,enemy)
        for enemy in enemies:
            if pygame.sprite.collide_rect(agent, enemy):
                enemy.kill()
                # destroy every object
                for obj in enemies:
                    obj.kill()
                game_ended = True
            for bullet in bullets:
                if pygame.sprite.collide_rect(bullet, enemy):
                    score += 10
                    bullet.kill()
                    # If an enemy is shot, spawn two new, smaller enemies
                    if enemy.scale == 150:
                        e1 = E.Enemy(100)
                        e2 = E.Enemy(100)
                        e1.pos_x, e1.pos_y = enemy.pos_x, enemy.pos_y
                        e2.pos_x, e2.pos_y = enemy.pos_x+50, enemy.pos_y+50
                        enemies.add(e1)
                        enemies.add(e2)
                        objects.add(e1)
                        objects.add(e2)
                        enemy.kill()
                    elif enemy.scale == 100:
                        e1 = E.Enemy(50)
                        e2 = E.Enemy(50)
                        e1.pos_x, e1.pos_y = enemy.pos_x, enemy.pos_y
                        e2.pos_x, e2.pos_y = enemy.pos_x+25, enemy.pos_y+25
                        enemies.add(e1)
                        enemies.add(e2)
                        objects.add(e1)
                        objects.add(e2)
                        enemy.kill()
                    else:
                        enemy.kill()
                        score += 40
        
        # If game is over, wait for agent to restart or quit the game
        if game_ended:
            # Draw background and gameover display
            screen.blit(bg, (0, 0))
            display = "GAME OVER! Your score is " + str(score) + "."
            gameover_display = font_over.render(display, True, (255,255,255))
            screen.blit(gameover_display, (WIDTH/2 - gameover_display.get_width()/2, 
                                           HEIGHT/2 - gameover_display.get_height()/2))
            screen.blit(again_display, (WIDTH/2 - again_display.get_width()/2, 
                                        HEIGHT/2 - again_display.get_height()/2 
                                        + gameover_display.get_height()))
            # Restart on 'r'
            if keys[pygame.K_r]:
                score = 0
                agent.pos_x, agent.pos_y = WIDTH//2, HEIGHT//2
                agent.rect = agent.img.get_rect(center=(agent.pos_x, agent.pos_y))
                screen.blit(agent.img, agent.rect)
                game_ended = False
        else:
            # Draw background image onto screen at top left corner
            screen.blit(bg, (0, 0))
            score_display = font_score.render(str(score), True, (255,255,255))

            # Update objects and draw on screen
            for obj in objects:
                obj.move()
                screen.blit(obj.img, obj.rect)
                
            # get observations
            get_obs(agent, enemies)
            
            # Draw score onto screen
            screen.blit(score_display, (10, 10))
        
        # Increase time vars every update
        clock.tick(FPS)
        time_count += 1
        shoot_count += 1
        
        # Update display every frame
        pygame.display.update()
    
    # Quit the game after application is not 'running' anymore
    pygame.quit()
    

# Main guard prevents running on import
if __name__ == "__main__":
    main()