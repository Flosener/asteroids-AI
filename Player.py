import pygame
import math


def update_direction(obj):
        """ Function to update the direction the spaceship is facing. """
        obj.rotated = pygame.transform.rotozoom(obj.img, obj.angle, 1)
        obj.rect = obj.rotated.get_rect(center=(obj.pos_x, obj.pos_y))
        obj.sin = math.sin(math.radians(obj.angle + 90))
        obj.cos = math.cos(math.radians(obj.angle + 90))
        obj.direction = (obj.pos_x + obj.cos * obj.scale/2, obj.pos_y - obj.sin * obj.scale/2)
        
        return [obj.direction, obj.angle, obj.sin, obj.cos]

        
class Player(pygame.sprite.Sprite):
    """ Player object class. """
    
    def __init__(self):
        """ Initialize a player object. """
        super().__init__()
        
        # load and scale player image
        self.scale = 50
        self.img = pygame.image.load("images/spaceship.png") #https://www.flaticon.com/premium-icon/space-ship_2949281?term=space%20ship&related_id=2949281
        self.img = pygame.transform.scale(self.img, (self.scale, self.scale))
        
        # get inital position of player in middle of screen
        self.pos_x = 600
        self.pos_y = 350
        
        # rotation and collision rectangle
        self.angle = 0
        self.rotated = pygame.transform.rotozoom(self.img, self.angle, 1) # rotozoom instead rotate improves quailty of rotated image
        self.rect = self.rotated.get_rect(center=(self.pos_x, self.pos_y))
        
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
        if self.pos_x >= 1200:
            self.pos_x = 1200
        if self.pos_y <= 0:
            self.pos_y = 0
        if self.pos_y >= 700:
            self.pos_y = 700
        
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