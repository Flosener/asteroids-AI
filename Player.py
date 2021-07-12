import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        """ Initialize a player object. """
        player_x = WIDTH/2
        player_y = HEIGHT/2
        scale = 50
        player_img = pygame.image.load("images/space-ship.png") # https://www.flaticon.com/premium-icon/space-ship_2949281?term=space%20ship&related_id=2949281
        player_img = pygame.transform.scale(player_img, (scale,scale))