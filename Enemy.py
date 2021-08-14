import pygame
from random import randint, randrange, sample
import helper as H


class Enemy(pygame.sprite.Sprite):
    """ Enemy object class for the asteroids game. """
    
    def __init__(self, scale):
        """ Initialize an asteroid object. """
        super().__init__()
        
        # Randomly scale the enemy (small, medium or large) and assign speed accordingly
        self.scale = scale
        self.speed = (1 if self.scale == 150 else 2 if self.scale == 100 else 3)
        # Asteroid: https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
        self.img = pygame.image.load("images/meteorite.png")
        self.img = pygame.transform.scale(self.img, (self.scale, self.scale))
        
        # Get initial random spawn position of enemy around the screen (x along the whole width, y only outside the borders)
        self.pos_x = randint(-self.scale, H.WIDTH + self.scale)
        self.pos_y = randint(-self.scale, 0) if randint(0,1) == 0 \
                        else randint(H.HEIGHT, H.HEIGHT + self.scale)
        # Moving direction: move to the right (down) if spawned on the left (top) and vice versa
        self.dir_x = 1 if self.pos_x <= H.WIDTH//2 else -1
        self.dir_y = 1 if self.pos_y <= H.HEIGHT//2 else -1
        
        # Collision rectangle
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))
        
        
    def move(self):
        """ Method to update the enemy position. """
        
        # Remove object at borders
        if (self.pos_x <= 0 - self.scale//2 and self.dir_x == -1):
            self.pos_x = H.WIDTH + self.scale//2
            self.pos_y = H.HEIGHT - self.pos_y
        if (self.pos_x >= H.WIDTH + self.scale//2 and self.dir_x == 1):
            self.pos_x = 0 - self.scale//2
            self.pos_y = H.HEIGHT - self.pos_y
        if (self.pos_y <= 0 - self.scale//2 and self.dir_y == -1):
            self.pos_x = H.WIDTH - self.pos_x
            self.pos_y = H.HEIGHT + self.scale//2
        if (self.pos_y >= H.HEIGHT + self.scale//2 and self.dir_y == 1):
            self.pos_x = H.WIDTH - self.pos_x
            self.pos_y = 0 - self.scale//2
        
        # Update position with according direction (depends on spawn pos)
        # Get some randomness into asteroid's speed
        self.pos_x += self.dir_x * self.speed * randrange(1,2)
        self.pos_y += self.dir_y * self.speed * randrange(1,2)
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))