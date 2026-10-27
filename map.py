
import pygame
import random
import math

WIDTH = 1000
HEIGHT = 650

# Forest colors
GREEN = (53, 65, 49)
DARK = (38, 48, 38)
TREE = (39, 61, 39)
TREE_LIGHT = (53, 76, 46)
TRUNK = (79, 57, 40)
GRASS = (83, 91, 59)
BUSH = (45, 62, 40)
ROCK = (83, 83, 72)
LEAF = (100, 91, 57)
SHADOW = (50, 57, 50)


def make_forest():
    trees = []

    random.seed(12)

    for _ in range(180):
        x = random.randint(-1400, 1400)
        y = random.randint(-1200, 1200)
        if -180 < x < 180 and -100 < y < 300:
            continue

        size = random.randint(20, 38)
        trees.append((x, y, size))

    random.seed()
    return trees


def draw_forest(screen, trees, camera):
    screen.fill(GREEN)

    # Ground details
    for i in range(300):
        x = (i * 137) % 2800 - 1400
        y = (i * 193) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if 0 < sx < WIDTH and 0 < sy < HEIGHT:
            pygame.draw.circle(
                screen, DARK, (int(sx), int(sy)), 2
            )

    # Grass patches
    for i in range(180):
        x = (i * 97) % 2800 - 1400
        y = (i * 151) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if -10 < sx < WIDTH + 10 and -10 < sy < HEIGHT + 10:
            pygame.draw.line(
                screen, GRASS,
                (int(sx), int(sy)),
                (int(sx + 4), int(sy - 5)), 2
            )

    # Fallen leaves
    for i in range(100):
        x = (i * 173) % 2800 - 1400
        y = (i * 109) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if 0 < sx < WIDTH and 0 < sy < HEIGHT:
            pygame.draw.ellipse(
                screen, LEAF,
                (int(sx), int(sy), 5, 3)
            )

    # Rocks and bushes
    for i in range(55):
        x = (i * 211) % 2800 - 1400
        y = (i * 157) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if -40 < sx < WIDTH + 40 and -40 < sy < HEIGHT + 40:
            if i % 2 == 0:
                pygame.draw.ellipse(
                    screen, ROCK,
                    (int(sx), int(sy), 20, 13)
                )
                pygame.draw.ellipse(
                    screen, DARK,
                    (int(sx + 3), int(sy + 8), 16, 5)
                )
            else:
                pygame.draw.circle(
                    screen, BUSH,
                    (int(sx), int(sy)), 13
                )
                pygame.draw.circle(
                    screen, TREE,
                    (int(sx - 4), int(sy - 3)), 8
                )

    # Fallen logs
    for i in range(16):
        x = (i * 347) % 2800 - 1400
        y = (i * 263) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if -80 < sx < WIDTH + 80 and -30 < sy < HEIGHT + 30:
            pygame.draw.line(
                screen, SHADOW,
                (int(sx), int(sy + 4)),
                (int(sx + 48), int(sy + 10)), 12
            )
            pygame.draw.line(
                screen, TRUNK,
                (int(sx), int(sy)),
                (int(sx + 48), int(sy + 6)), 8
            )
            pygame.draw.circle(
                screen, (105, 78, 51),
                (int(sx + 48), int(sy + 6)), 4
            )

    # Trees
    for tree in trees:
        x, y, size = tree

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if (
            sx < -size - 20 or sx > WIDTH + size + 20
            or sy < -size - 40 or sy > HEIGHT + size + 40
        ):
            continue

        # Tree shadow
        pygame.draw.ellipse(
            screen, SHADOW,
            (int(sx - size), int(sy + 8),
             size * 2 + 18, size + 12)
        )

        # Trunk
        pygame.draw.rect(
            screen, TRUNK,
            (int(sx - 6), int(sy + 5), 12, size + 13)
        )

        # Main canopy
        pygame.draw.circle(
            screen, TREE,
            (int(sx), int(sy)), size
        )

        # Highlights
        pygame.draw.circle(
            screen, TREE_LIGHT,
            (int(sx - size // 3), int(sy - size // 4)),
            max(5, size // 2)
        )

        pygame.draw.circle(
            screen, BUSH,
            (int(sx + size // 3), int(sy + size // 4)),
            max(4, size // 3)
        )

        # Small canopy details
        pygame.draw.circle(
            screen, TREE,
            (int(sx + size // 2), int(sy - size // 3)),
            max(4, size // 3)
        )
