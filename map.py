import pygame
import random

## map colors
GREEN = (67, 72, 61)
DARK = (42, 48, 41)
TREE = (48, 68, 46)
TRUNK = (82, 62, 45)

WIDTH = 1000
HEIGHT = 650

## create trees
def make_forest():
    trees = []

    for _ in range(100):
        ## spawn trees at a random x and y range
        x = random.randint(-1000, 1000)
        y = random.randint(-800, 800)

        # don't spawn trees near the player
        if -180 < x < 180 and 0 < y < 300:
            continue

        trees.append((x, y))

    return trees

## make the map (forest)
def draw_forest(screen, trees, camera):
    screen.fill(GREEN)

    # ground details
    for i in range(100):
        x = (i * 83) % 2000 - 1000
        y = (i * 137) % 1600 - 800

        screen_x = x - camera.x + WIDTH // 2
        screen_y = y - camera.y + HEIGHT // 2

        if (
            0 < screen_x < WIDTH
            and 60 < screen_y < HEIGHT
        ):
            pygame.draw.circle(
                screen,
                DARK,
                (int(screen_x), int(screen_y)),
                3
            )

    # trees
    for x, y in trees:
        screen_x = x - camera.x + WIDTH // 2
        screen_y = y - camera.y + HEIGHT // 2

        # don't create trees outside of screen
        if (
            screen_x < -70
            or screen_x > WIDTH + 70
            or screen_y < -70
            or screen_y > HEIGHT + 70
        ):
            continue

        # trunk and leaves
        pygame.draw.rect(
            screen,
            TRUNK,
            (
                screen_x - 7,
                screen_y + 10,
                14,
                35
            )
        )
        pygame.draw.circle(
            screen,
            TREE,
            (int(screen_x), int(screen_y)),
            29
        )
