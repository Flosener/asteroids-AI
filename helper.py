import pygame


# Pygame global variables
WIDTH = 1200
HEIGHT = 700
FPS = 60

# Pygame settings
pygame.font.init()
font_over = pygame.font.Font('resources/Pixeltype.ttf', 60)
font_score = pygame.font.Font('resources/Pixeltype.ttf', 30)
again_display = font_score.render("Press 'r' to restart.", True, (255,255,255))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Background: https://wallpapertag.com/wallpaper/full/a/5/b/547899-large-star-sky-wallpaper-3100x1740-4k.jpg
bg = pygame.image.load("resources/star_sky.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Hyperparameters for AI
N_EPOCHS = 10
N_AGENTS = 15
N_INPUTS = 3
N_HIDDEN = 5
N_OUTPUTS = 3
MUTATION_RATE = 0.05