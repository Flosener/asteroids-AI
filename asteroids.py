import pygame

# import object classes
import Player
import Enemy


def main():
    """ The main function of our asteroids game. """
    WIDTH = 1200
    HEIGHT = 700
    SCORE = 0
    
    # Initialize pygame
    pygame.init()
    
    # Fix FPS
    clock = pygame.time.Clock()
    FPS = 60

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
    
    # Adding player
    player = Player.Player()
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Set background color to maroon (not necessary if we use background img)
        # screen.fill((128,0,0))
        
        # Blit background image onto screen at top left corner + player
        screen.blit(bg, (0, 0))
        screen.blit(player.img, (int(player.pos_x - player.scale/2), int(player.pos_y - player.scale/2)))
        player.update()
        
        """
        for obj in objects:
            screen.blit(obj.img, obj.rect)
            obj.move()
        
        # collision: draw end screen, remove all objects and end game
        if pygame.sprite.spritecollideany(player, enemies):
            screen.blit(game_over, (WIDTH/2, HEIGHT/2))
            #pygame.display.update()
            
            for obj in objects:
                obj.kill()
            running = False
        """
        
        clock.tick(FPS)
        
        # Update all GUI elements
        pygame.display.update()
    
    # Quit the game after application is not 'running' anymore
    pygame.quit()
    
    
# main guard prevents running on import
if __name__ == "__main__":
    main()