import pygame

WIDTH, HEIGHT = 1000, 650
FPS = 60

GREEN = (67, 72, 61)
DARK = (42, 48, 41)
TREE = (48, 68, 46)
TRUNK = (82, 62, 45)
WHITE = (235, 235, 225)
RED = (190, 45, 45)
BLACK = (20, 20, 20)
YELLOW = (235, 205, 70)

def create_fonts():
    return {
        "normal": pygame.font.Font(None, 36),
        "big": pygame.font.Font(None, 90),
        "small": pygame.font.Font(None, 24),
    }