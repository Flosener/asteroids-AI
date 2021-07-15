import pygame
# import player class and main()
import Player as P
import asteroids as M


class Bullet(pygame.sprite.Sprite):
    """ Bullet object class. """
    
    def __init__(self, player):
        """ Initialize a bullet object. """
        super().__init__()
        
        # load and scale bullet image
        self.scale = 20
        self.img = pygame.image.load("images/bullet.png")
        self.img = pygame.transform.scale(self.img, (self.scale//2, self.scale))
        
        # initial bullet position and rotation is the spaceship's head (direction) and angle
        self.direction = P.update_direction(player)[0]
        self.angle = P.update_direction(player)[1]
        self.sin = P.update_direction(player)[2]
        self.cos = P.update_direction(player)[3]
        self.pos_x, self.pos_y = self.direction
        self.img = pygame.transform.rotozoom(self.img, self.angle, 1)
        
        
        # collision rect and speed
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))
        self.speed = 7
        
    
    def move(self):
        """ Method to update position of bullet. """
        # remove object at borders
        if self.pos_x <= 0 or self.pos_x >= M.WIDTH:
            self.kill()
        if self.pos_y <= 0 or self.pos_y >= M.HEIGHT:
            self.kill()
        
        # use player's cosine and sine for updating bullet position
        self.pos_x += self.cos * self.speed
        self.pos_y -= self.sin * self.speed
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))
        
            
        