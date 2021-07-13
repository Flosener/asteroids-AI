import pygame
from random import randint, sample

class Enemy(pygame.sprite.Sprite):
    """ Enemy object class. """
    
    def __init__(self):
        """ Initialize a player object. """
        super().__init__()
        
        # get initial spawn position of enemy (50 pixels around screen)
        self.pos_x = randint(-50, 0) if randint(0,1) == 0 else randint(700, 750)
        self.pos_y = randint(-50, 0) if randint(0,1) == 0 else randint(1200, 1250)
        
        # randomly scale the enemy (small, medium or large) and assign speed accordingly
        self.scale = sample([10, 25, 50], k=1)[0]
        self.speed = 2 if self.scale == 50 else 4 if self.scale == 25 else 10 
        self.img = pygame.image.load("images/meteorite.png") # https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
        self.img = pygame.transform.scale(self.img, (self.scale, self.scale))
        
        # get surface and rectangle for collision detection
        self.surf = pygame.Surface((self.scale, self.scale))
        self.rect = self.surf.get_rect()
        
        
    def update(self):
        """ Method to update enemy movement. """
        pass