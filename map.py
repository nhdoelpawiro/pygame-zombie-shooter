
import pygame
import random
import math

WIDTH = 1000
HEIGHT = 650

# Map boundaries
MAP_LEFT = -1000
MAP_RIGHT = 1000
MAP_TOP = -800
MAP_BOTTOM = 800

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
BLACK = (0, 0, 0)


def make_forest():
    trees = []
    rng = random.Random(12)

    # Generate trees only inside the playable map
    for _ in range(40):
        x = rng.randint(MAP_LEFT + 40, MAP_RIGHT - 40)
        y = rng.randint(MAP_TOP + 40, MAP_BOTTOM - 40)

        # Keep the player's starting area clear
        if -180 < x < 180 and -100 < y < 300:
            continue

        size = rng.randint(20, 38)
        trees.append((x, y, size))

    return trees


def draw_forest(screen, trees, camera):
    # Make everything outside the map black
    screen.fill(BLACK)

    # Convert world boundaries to screen coordinates
    left = MAP_LEFT - camera.x + WIDTH // 2
    right = MAP_RIGHT - camera.x + WIDTH // 2
    top = MAP_TOP - camera.y + HEIGHT // 2
    bottom = MAP_BOTTOM - camera.y + HEIGHT // 2

    map_rect = pygame.Rect(
        round(left),
        round(top),
        round(right - left),
        round(bottom - top)
    )

    # Restrict all forest drawing to the playable map
    old_clip = screen.get_clip()
    screen.set_clip(old_clip.clip(map_rect))

    # Ground
    screen.fill(GREEN)

    # Ground details
    for i in range(300):
        x = (i * 137) % 2800 - 1400
        y = (i * 193) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if 0 < sx < WIDTH and 0 < sy < HEIGHT:
            pygame.draw.circle(
                screen,
                DARK,
                (int(sx), int(sy)),
                2
            )

    # Grass patches
    for i in range(180):
        x = (i * 97) % 2800 - 1400
        y = (i * 151) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if -10 < sx < WIDTH + 10 and -10 < sy < HEIGHT + 10:
            pygame.draw.line(
                screen,
                GRASS,
                (int(sx), int(sy)),
                (int(sx + 4), int(sy - 5)),
                2
            )

    # Fallen leaves
    for i in range(100):
        x = (i * 173) % 2800 - 1400
        y = (i * 109) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if 0 < sx < WIDTH and 0 < sy < HEIGHT:
            pygame.draw.ellipse(
                screen,
                LEAF,
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
                    screen,
                    ROCK,
                    (int(sx), int(sy), 20, 13)
                )

                pygame.draw.ellipse(
                    screen,
                    DARK,
                    (int(sx + 3), int(sy + 8), 16, 5)
                )
            else:
                pygame.draw.circle(
                    screen,
                    BUSH,
                    (int(sx), int(sy)),
                    13
                )

                pygame.draw.circle(
                    screen,
                    TREE,
                    (int(sx - 4), int(sy - 3)),
                    8
                )

    # Fallen logs
    for i in range(16):
        x = (i * 347) % 2800 - 1400
        y = (i * 263) % 2400 - 1200

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if -80 < sx < WIDTH + 80 and -30 < sy < HEIGHT + 30:
            pygame.draw.line(
                screen,
                SHADOW,
                (int(sx), int(sy + 4)),
                (int(sx + 48), int(sy + 10)),
                12
            )

            pygame.draw.line(
                screen,
                TRUNK,
                (int(sx), int(sy)),
                (int(sx + 48), int(sy + 6)),
                8
            )

            pygame.draw.circle(
                screen,
                (105, 78, 51),
                (int(sx + 48), int(sy + 6)),
                4
            )

    # Trees
    for tree in trees:
        x, y, size = tree

        sx = x - camera.x + WIDTH // 2
        sy = y - camera.y + HEIGHT // 2

        if (
            sx < -size - 20
            or sx > WIDTH + size + 20
            or sy < -size - 40
            or sy > HEIGHT + size + 40
        ):
            continue

        # Tree shadow
        pygame.draw.ellipse(
            screen,
            SHADOW,
            (
                int(sx - size),
                int(sy + 8),
                size * 2 + 18,
                size + 12
            )
        )

        # Trunk
        pygame.draw.rect(
            screen,
            TRUNK,
            (
                int(sx - 6),
                int(sy + 5),
                12,
                size + 13
            )
        )

        # Main canopy
        pygame.draw.circle(
            screen,
            TREE,
            (int(sx), int(sy)),
            size
        )

        # Canopy highlights
        pygame.draw.circle(
            screen,
            TREE_LIGHT,
            (
                int(sx - size // 3),
                int(sy - size // 4)
            ),
            max(5, size // 2)
        )

        pygame.draw.circle(
            screen,
            BUSH,
            (
                int(sx + size // 3),
                int(sy + size // 4)
            ),
            max(4, size // 3)
        )

        # Small canopy detail
        pygame.draw.circle(
            screen,
            TREE,
            (
                int(sx + size // 2),
                int(sy - size // 3)
            ),
            max(4, size // 3)
        )

    # Restore normal drawing area
    screen.set_clip(old_clip)
