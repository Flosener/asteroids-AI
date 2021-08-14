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
# screen and background
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Background: https://wallpapertag.com/wallpaper/full/a/5/b/547899-large-star-sky-wallpaper-3100x1740-4k.jpg
bg = pygame.image.load("images/star_sky.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Hyperparameters for AI
N_AGENTS = 10
N_INPUTS = 3
N_HIDDEN = 5
N_OUTPUTS = 3
MUTATION_RATE = 0.05
N_EPOCHS = 10