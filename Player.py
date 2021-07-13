import pygame
import Bullet

class Player(pygame.sprite.Sprite):
    """ Player object class. """
    
    def __init__(self):
        """ Initialize a player object. """
        super().__init__()
        
        # get inital position of player in middle of screen
        self.pos_x = 600
        self.pos_y = 350
        
        # load and scale player image
        self.scale = 50
        self.img = pygame.image.load("images/space-ship.png") #https://www.flaticon.com/premium-icon/space-ship_2949281?term=space%20ship&related_id=2949281
        self.img = pygame.transform.scale(self.img, (self.scale, self.scale))
        
        # get surface and rectangle for collision detection
        self.surf = pygame.Surface((self.scale, self.scale))
        self.rect = self.surf.get_rect()
        
        
    def update(self):
        """ Method to check for user input and move our player object (position and rotation) or shoot. """
        keys = pygame.key.get_pressed()
        
        # Shooting
        if keys[pygame.K_SPACE]:
            #bullet = Bullet.Bullet()
            print("Pow! Pow!")
        
        # Moving forward and backward
        if keys[pygame.K_w]:
            print("forward")
        if keys[pygame.K_s]:
            print("backward")
        
        # Rotating
        if keys[pygame.K_a]:
            print("left")
        if keys[pygame.K_d]:
            print("right")
            