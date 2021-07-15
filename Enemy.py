import pygame
from random import randint, randrange, sample
# import main()
import asteroids as M


class Enemy(pygame.sprite.Sprite):
    """ Enemy object class. """
    
    def __init__(self, diff, scale):
        """ Initialize a player object. """
        super().__init__()
        
        # randomly scale the enemy (small, medium or large) and assign speed accordingly
        self.scale = scale
        self.speed = (1 if self.scale == 150 else 2 if self.scale == 100 else 3) * diff
        self.img = pygame.image.load("images/meteorite.png") # https://www.flaticon.com/free-icon/meteorite_4260653?term=asteroids&related_id=4260653
        self.img = pygame.transform.scale(self.img, (self.scale, self.scale))
        
        # get initial spawn position of enemy (self.scale pixels around screen)
        self.pos_x = randint(-self.scale, 0) if randint(0,1) == 0 else randint(M.WIDTH, M.WIDTH + self.scale)
        self.pos_y = randint(-self.scale, 0) if randint(0,1) == 0 else randint(M.HEIGHT, M.HEIGHT + self.scale)
        # moving direction: move to the right (down) if spawned on the left (top) and vice versa
        self.dir_x = 1 if self.pos_x <= M.WIDTH//2 else -1
        self.dir_y = 1 if self.pos_y <= M.HEIGHT//2 else -1
        
        # collision rectangle
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))
        
        
    def move(self):
        """ Method to update enemy movement. """
        
        # remove object at borders
        if (self.pos_x <= 0 - self.scale//2 and self.dir_x == -1) or (self.pos_x >= M.WIDTH + self.scale//2 and self.dir_x == 1):
            self.kill()
        if (self.pos_y <= 0 - self.scale//2 and self.dir_y == -1) or (self.pos_y >= M.HEIGHT + self.scale//2 and self.dir_y == 1):
            self.kill()
        
        # update position with according direction (depends on spawn pos)
        self.pos_x += self.dir_x * self.speed * randrange(1,2) # get some randomness into asteroid's speed
        self.pos_y += self.dir_y * self.speed * randrange(1,2)
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))