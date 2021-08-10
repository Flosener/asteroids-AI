import pygame
import Agent as A
import asteroids as M


class Bullet(pygame.sprite.Sprite):
    """ Bullet object class for the asteroids game. """
    
    def __init__(self, agent):
        """ Initialize a bullet object. """
        super().__init__()
        
        # Load and scale bullet image
        self.scale = 20
        # Bullet: https://www.flaticon.com/free-icon/bullet_224681?term=bullet&page=1&position=1&page=1&position=1&related_id=224681&origin=search
        self.img = pygame.image.load("images/bullet.png")
        self.img = pygame.transform.scale(self.img, (self.scale//2, self.scale))
        
        # Initial bullet position/rotation is the spaceship's direction/angle
        self.direction, self.angle, self.sin, self.cos = A.update_direction(agent)
        self.pos_x, self.pos_y = self.direction
        self.img = pygame.transform.rotozoom(self.img, self.angle, 1)
        
        # Collision rect and speed
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))
        self.speed = 7
        
    
    def move(self):
        """ Method to update position of bullet. """
        # Remove object at borders
        if self.pos_x <= 0 or self.pos_x >= M.WIDTH:
            self.kill()
        if self.pos_y <= 0 or self.pos_y >= M.HEIGHT:
            self.kill()
        
        # Use agent's cosine and sine for updating bullet position
        self.pos_x += self.cos * self.speed
        self.pos_y -= self.sin * self.speed
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))
        
            
        