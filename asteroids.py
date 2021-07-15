import pygame
from random import sample
# import object classes
import Player as P
import Enemy as E
import Bullet as B

# Global screen vars
WIDTH = 1200
HEIGHT = 700


def main():
    """ The main function of our asteroids game. """
    # Optional: Ask for difficulty in terminal
    try:
        diff = int(input("Choose your difficulty! 1: easy, 2: medium, 3: hard." ))
        if type(diff) != int:
            raise ValueError
    except ValueError:
        diff = 1
        print("That was no integer. You now play on default: easy!")
    
    # Initialize pygame
    pygame.init()
    
    # Fix FPS
    clock = pygame.time.Clock()
    FPS = 60
    
    # gameloop vars
    shoot_count = 0
    time_count = 0
    lives = 3
    score = 0
    game_ended = False

    # Create game window screen
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    
    # Title, icon, background
    pygame.display.set_caption("Asteroids")
    img = pygame.image.load("images/meteorite.png") # https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
    pygame.display.set_icon(img)
    bg = pygame.image.load("images/star_sky.jpg") # https://wallpapertag.com/wallpaper/full/a/5/b/547899-large-star-sky-wallpaper-3100x1740-4k.jpg
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT)) # scale background to fit game display screen size
    
    # score and lives display
    font_over = pygame.font.SysFont("Georgia", 60)
    font_score = pygame.font.SysFont("Georgia", 30)
    font_lives = pygame.font.SysFont("Georgia", 15)
    again_display = font_score.render("Press 'r' to restart.", True, (255,255,255))
    
    # Setup sprite groups for use in collision detection
    objects = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = P.Player()
    objects.add(player)
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        keys = pygame.key.get_pressed()
        
        # shooting only possible every third of a second
        if shoot_count >= FPS//3:
            # shoot on space
            if keys[pygame.K_SPACE]:
                # spawn bullet from player and add to sprite groups for collision
                bullet = B.Bullet(player)
                objects.add(bullet)
                bullets.add(bullet)
                shoot_count = 0
        
        # spawn enemies every 2 seconds
        if time_count >= FPS*2:
            scale = sample([50, 100, 150], k=1)[0]
            enemy = E.Enemy(diff, scale)
            objects.add(enemy)
            enemies.add(enemy)
            time_count = 0
            
        # player/asteroid (death) collision detection
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                enemy.kill()
                lives -= 1
                if lives == 0:
                    # destroy every object
                    for obj in enemies:
                        obj.kill()
                    game_ended = True

        # bullet/asteroid (score) collision detection
        for bullet in bullets:
            for enemy in enemies:
                if pygame.sprite.collide_rect(bullet, enemy):
                    score += 10
                    bullet.kill()
                    if enemy.scale == 150:
                        e1 = E.Enemy(diff, 100)
                        e2 = E.Enemy(diff, 100)
                        e1.pos_x, e1.pos_y = enemy.pos_x, enemy.pos_y
                        e2.pos_x, e2.pos_y = enemy.pos_x, enemy.pos_y
                        enemies.add(e1)
                        enemies.add(e2)
                        objects.add(e1)
                        objects.add(e2)
                        enemy.kill()
                    elif enemy.scale == 100:
                        e1 = E.Enemy(diff, 50)
                        e2 = E.Enemy(diff, 50)
                        e1.pos_x, e1.pos_y = enemy.pos_x, enemy.pos_y
                        e2.pos_x, e2.pos_y = enemy.pos_x, enemy.pos_y
                        enemies.add(e1)
                        enemies.add(e2)
                        objects.add(e1)
                        objects.add(e2)
                        enemy.kill()
                    else:
                        enemy.kill()
                        score += 40
        
        # if game over, wait for player to restart or quit the game
        if game_ended:
            # draw background and gameover display
            screen.blit(bg, (0, 0))
            gameover_display = font_over.render("GAME OVER! Your score is " + str(score) + ".", True, (255,255,255))
            screen.blit(gameover_display, (WIDTH/2 - gameover_display.get_width()/2, 
                                           HEIGHT/2 - gameover_display.get_height()/2))
            screen.blit(again_display, (WIDTH/2 - again_display.get_width()/2, 
                                        HEIGHT/2 - again_display.get_height()/2 + gameover_display.get_height()))
            
            # restart on 'r'
            if keys[pygame.K_r]:
                score = 0
                lives = 3
                #player.pos_x, player.pos_y = WIDTH//2, HEIGHT//2
                game_ended = False
        else:
            # Draw background image onto screen at top left corner
            screen.blit(bg, (0, 0))
            score_display = font_score.render(str(score), True, (255,255,255))
            lives_display = font_lives.render("Lives: " + str(lives), True, (255,255,255))

            # update objects and draw on screen
            for obj in objects:
                obj.move()
                screen.blit(obj.img, obj.rect)
            
            # draw score and lives onto screen
            screen.blit(score_display, (10, 10))
            screen.blit(lives_display, (10, 40))
        
        # increase time vars every update
        clock.tick(FPS)
        time_count += 1
        shoot_count += 1
        
        # update display every frame
        pygame.display.update()
    
    # Quit the game after application is not 'running' anymore
    pygame.quit()
    
    
# main guard prevents running on import
if __name__ == "__main__":
    main()