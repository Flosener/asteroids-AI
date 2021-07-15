import pygame
import math
# import main()
import asteroids as M

def update_direction(obj):
        """ Function to update the direction the spaceship is facing. """
        obj.img = pygame.transform.rotozoom(obj.image, obj.angle, 1)
        obj.rect = obj.img.get_rect(center=(obj.pos_x, obj.pos_y))
        obj.sin = math.sin(math.radians(obj.angle + 90))
        obj.cos = math.cos(math.radians(obj.angle + 90))
        obj.direction = (obj.pos_x + obj.cos * obj.scale/2, obj.pos_y - obj.sin * obj.scale/2)
        
        # return list to be used in Bullet class
        return [obj.direction, obj.angle, obj.sin, obj.cos]

        
class Player(pygame.sprite.Sprite):
    """ Player object class. """
    
    def __init__(self):
        """ Initialize a player object. """
        super().__init__()
        
        # load and scale player image
        self.scale = 50
        self.image = pygame.image.load("images/spaceship.png") # https://www.flaticon.com/free-icon/spaceship_901787
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        
        # get inital position of player in middle of screen
        self.pos_x = M.WIDTH//2
        self.pos_y = M.HEIGHT//2
        
        # rotation and collision rectangle
        self.angle = 0
        self.img = pygame.transform.rotozoom(self.image, self.angle, 1) # rotozoom instead rotate improves quailty of rotated image
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))
        
        # track the direction the spaceship is facing for forward movement
        # calculate the sine/cosine of the radians of the angle by which the spaceship is turning
        # add this to the current position for x and y
        self.speed = 5
        self.sin = math.sin(math.radians(self.angle + 90))
        self.cos = math.cos(math.radians(self.angle + 90))
        self.direction = (self.pos_x + self.cos * self.scale/2, self.pos_y - self.sin * self.scale/2)
        
        
    def move(self):
        """ Method to check for user input and move our player object (position and rotation). """
        # if player is at screen borders, it cannot move further
        if self.pos_x <= 0:
            self.pos_x = 0
        if self.pos_x >= M.WIDTH:
            self.pos_x = M.WIDTH
        if self.pos_y <= 0:
            self.pos_y = 0
        if self.pos_y >= M.HEIGHT:
            self.pos_y = M.HEIGHT
        
        keys = pygame.key.get_pressed()
        
        # Moving forward
        if keys[pygame.K_w]:
            self.pos_x += self.cos * self.speed
            self.pos_y -= self.sin * self.speed
            update_direction(self)
            
        # Rotating
        if keys[pygame.K_a]:
            self.angle += 5
            update_direction(self)
            
        if keys[pygame.K_d]:
            self.angle -= 5
            update_direction(self)