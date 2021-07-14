import pygame
import time

# import object classes
import Player as P
import Enemy as E
import Bullet as B


# global vars
WIDTH = 1200
HEIGHT = 700
SCORE = 0

def update_all(screen, background, player, allObjects, enemyObjects, bulletObjects):
    """ Function to update all GUI elements and objects. 
    
    Args:
    screen -- the window surface to draw on
    allObjects -- sprite group of spawned objects in the game
    """
    # Draw background image onto screen at top left corner
    screen.blit(background, (0, 0))
    
    # update objects and draw on screen
    for obj in allObjects:
        obj.move()
    for obj in enemyObjects:
        screen.blit(obj.img, obj.rect)
    for obj in bulletObjects:
        screen.blit(obj.img, obj.rect)
    
    # player only
    screen.blit(player.rotated, player.rect)
    pygame.draw.rect(screen, (255,0,0), player.rect, 2)
    
    pygame.display.update()

    
def main():
    """ The main function of our asteroids game. """
    
    # Initialize pygame
    pygame.init()
    
    # Fix FPS
    clock = pygame.time.Clock()
    FPS = 60
    count = 0

    # Create game window screen
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    
    # Title, icon, background
    pygame.display.set_caption("Asteroids")
    img = pygame.image.load("images/meteorite.png") # https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
    pygame.display.set_icon(img)
    bg = pygame.image.load("images/star_sky.jpg") # https://wallpapertag.com/wallpaper/full/a/5/b/547899-large-star-sky-wallpaper-3100x1740-4k.jpg
    # scale background to fit game display screen size
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    
    # Game-over and score display
    font_over = pygame.font.SysFont("Georgia", 60)
    font_score = pygame.font.SysFont("Georgia", 20)
    display = "Congrats! Your highscore is " + str(SCORE) + "."
    game_over = font_over.render(display, True, (0,0,0))
    
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
        
        # only every half second
        if count >= FPS//2:
            # shoot on space
            if keys[pygame.K_SPACE]:
                # spawn bullet from player and add to sprite groups for collision
                bullet = B.Bullet(player)
                objects.add(bullet)
                bullets.add(bullet)
                count = 0
        
        """
        # death collision detection
        if pygame.sprite.spritecollideany(player, enemies):
            screen.blit(game_over, (WIDTH/2, HEIGHT/2))
            
            # destroy every object
            for obj in objects:
                obj.kill()
            running = False
            
        # score collision detection
        if pygame.sprite.groupcollide(bullets, enemies, True, False):
            SCORE += 10
            
            # destroy every object
            for obj in bullets:
                obj.kill()
            for obj in enemies:
                if obj.scale == 50:
                    obj.scale = 25
                elif obj.scale == 25:
                    obj.scale = 10
                else:
                    obj.kill()
        """
        
        clock.tick(FPS)
        count += 1
        
        # Update all objects and GUI
        update_all(screen, bg, player, objects, enemies, bullets)
    
    # Quit the game after application is not 'running' anymore
    pygame.quit()
    
    
# main guard prevents running on import
if __name__ == "__main__":
    main()