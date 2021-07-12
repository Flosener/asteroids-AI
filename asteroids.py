import pygame

# Global vars
WIDTH = 1200
HEIGHT = 700

def main():
    """ The main function of our game. """
    # Initialize pygame
    pygame.init()
    
    # Fix FPS
    FPS = 60
    clock = pygame.time.Clock()

    # Create game window screen (width,height)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    
    # Title, icon, background
    pygame.display.set_caption("Asteroids")
    img = pygame.image.load("images/meteorite.png") # https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
    pygame.display.set_icon(img)
    bg = pygame.image.load("images/star_sky.jpg") # https://wallpapertag.com/wallpaper/full/a/5/b/547899-large-star-sky-wallpaper-3100x1740-4k.jpg
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT)) # scale background to fit game display screen size
    

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
        screen.blit(player_img, (int(player_x - scale/2), int(player_y - scale/2)))
        
        clock.tick(FPS)
        
        # Update all GUI elements
        pygame.display.update()
    
    # Quit the game after application is not 'running' anymore
    pygame.quit()

    
# main guard prevents running on import
if __name__ == "__main__":
    main()