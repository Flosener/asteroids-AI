import pygame
import os

# change current working directory to use relative path
# https://stackoverflow.com/questions/64835525/is-there-any-other-way-to-load-a-resource-like-an-image-sound-or-font-into-pyg
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(sourceFileDir)
fontPath = os.path.join(sourceFileDir, 'Pixeltype.ttf')

# pygame globals
WIDTH = 1200
HEIGHT = 700
FPS = 60

# Score display
# https://www.dafont.com/pixeltype.font
font_over = pygame.font.SysFont(fontPath, 60)
font_score = pygame.font.SysFont(fontPath, 30)
again_display = font_score.render("Press 'r' to restart.", True, (255,255,255))

# Hyperparameters for AI
N_AGENTS = 10