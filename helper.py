import pygame

# pygame globals
WIDTH = 1200
HEIGHT = 700
FPS = 60

# Score display
pygame.font.init()
font_over = pygame.font.Font('Pixeltype.ttf', 60)
font_score = pygame.font.Font('Pixeltype.ttf', 30)
again_display = font_score.render("Press 'r' to restart.", True, (255,255,255))

# Hyperparameters for AI
N_AGENTS = 2