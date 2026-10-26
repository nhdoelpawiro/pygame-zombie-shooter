
import pygame
import random
import sys

pygame.init()

WIDTH = 1000
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcane Zaun Map - Rooftop View")
clock = pygame.time.Clock()

# Colors
GROUND = (25, 27, 33)
GROUND_LIGHT = (40, 44, 52)
GROUND_DARK = (15, 17, 21)
BUILDING = (42, 38, 52)
ROOF = (30, 27, 38)
WALL = (65, 55, 75)
WINDOW = (255, 170, 60)
NEON = (180, 40, 130)
BLUE = (0, 200, 220)
METAL = (60, 65, 75)
WOOD = (70, 50, 40)
FOUNTAIN = (50, 60, 70)
WATER = (30, 140, 160)
LIGHT = (255, 210, 120)
PLAYER_COLOR = (255, 100, 100)

# Buildings: x, y, width, height, shop
BUILDINGS = [
    (-950, -750, 300, 210, False),
    (-600, -750, 260, 210, True),
    (-250, -750, 300, 210, False),
    (100, -750, 300, 210, True),
    (450, -750, 300, 210, False),
    (750, -750, 250, 210, True),

    (-950, 540, 300, 240, True),
    (-600, 540, 260, 240, False),
    (-250, 540, 300, 240, True),
    (100, 540, 300, 240, False),
    (450, 540, 300, 240, True),
    (750, 540, 250, 240, False),

    (-1000, -400, 250, 250, True),
    (-1000, 0, 250, 250, False),
    (-1000, 350, 250, 200, True),

    (750, -400, 250, 250, False),
    (750, 0, 250, 250, True),
    (750, 350, 250, 200, False)
]

# Cars: x, y, direction
# 0 = vertical, 1 = horizontal
CARS = [
    (-350, -220, 0),
    (340, -260, 1),
    (-410, 270, 1),
    (400, 320, 0),
    (250, 100, 1)
]

PROPS = [
    (-250, -180), (220, -180),
    (-300, 160), (300, 180),
    (-150, 300), (160, 280),
    (-420, 40), (430, -20)
]


# Camera follows the player
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y):
        self.x += (target_x - self.x) * 0.1
        self.y += (target_y - self.y) * 0.1


def make_forest():
    objects = []
    random.seed(10)

    for i in range(100):
        x = random.randint(-950, 950)
        y = random.randint(-750, 750)

        if not (-170 < x < 170 and -130 < y < 130):
            objects.append((x, y, random.randint(1, 3)))

    return objects


def world_to_screen(x, y, camera):
    return (
        int(x - camera.x + WIDTH // 2),
        int(y - camera.y + HEIGHT // 2)
    )


def draw_car(screen, x, y, direction, camera):
    sx, sy = world_to_screen(x, y, camera)
    car = pygame.Surface((40, 64), pygame.SRCALPHA)

    pygame.draw.rect(car, (10, 10, 12, 140),
                     (5, 5, 32, 54), border_radius=10)

    # Tires
    pygame.draw.rect(car, (15, 16, 20), (2, 13, 8, 15), border_radius=3)
    pygame.draw.rect(car, (15, 16, 20), (30, 13, 8, 15), border_radius=3)
    pygame.draw.rect(car, (15, 16, 20), (2, 39, 8, 15), border_radius=3)
    pygame.draw.rect(car, (15, 16, 20), (30, 39, 8, 15), border_radius=3)

    # Car body
    pygame.draw.rect(car, (75, 80, 90), (6, 3, 28, 56), border_radius=9)
    pygame.draw.rect(car, (110, 115, 125), (9, 5, 22, 52), 2, border_radius=7)

    # Windows
    pygame.draw.rect(car, (90, 95, 105), (10, 7, 20, 13), border_radius=4)
    pygame.draw.polygon(car, (20, 25, 35),
                        [(10, 21), (30, 21), (28, 31), (12, 31)])
    pygame.draw.polygon(car, (20, 25, 35),
                        [(12, 35), (28, 35), (30, 44), (10, 44)])

    pygame.draw.line(car, (50, 55, 65), (11, 33), (29, 33), 2)

    # Lights
    pygame.draw.rect(car, (100, 240, 255), (9, 4, 7, 4), border_radius=2)
    pygame.draw.rect(car, (100, 240, 255), (24, 4, 7, 4), border_radius=2)
    pygame.draw.rect(car, (220, 40, 60), (9, 54, 7, 3), border_radius=1)
    pygame.draw.rect(car, (220, 40, 60), (24, 54, 7, 3), border_radius=1)

    if direction == 1:
        car = pygame.transform.rotate(car, 90)

    if -80 < sx < WIDTH + 80 and -80 < sy < HEIGHT + 80:
        screen.blit(car, car.get_rect(center=(sx, sy)))


def draw_building(screen, x, y, w, h, camera, shop=False):
    sx, sy = world_to_screen(x, y, camera)

    if sx + w < -100 or sx > WIDTH + 100:
        return

    if sy + h < -100 or sy > HEIGHT + 100:
        return

    # Shadow and building
    pygame.draw.rect(screen, (10, 12, 16), (sx + 12, sy + 14, w, h))
    pygame.draw.rect(screen, BUILDING, (sx, sy, w, h))
    pygame.draw.rect(screen, ROOF, (sx + 5, sy + 5, w - 10, h - 10))
    pygame.draw.rect(screen, WALL, (sx + 10, sy + 10, w - 20, 6))

    # Windows
    for wx in range(sx + 15, sx + w - 10, 25):
        for wy in range(sy + 18, sy + h - 10, 28):
            pygame.draw.rect(screen, WINDOW, (wx, wy, 9, 12))
            pygame.draw.rect(screen, (50, 40, 35), (wx, wy + 12, 9, 2))

    # Neon shop signs
    if shop:
        pygame.draw.rect(screen, NEON,
                         (sx + 10, sy + h - 22, w - 20, 8),
                         border_radius=3)
        pygame.draw.rect(screen, BLUE,
                         (sx + 15, sy + h - 14, w - 30, 3))


def draw_map(screen, objects, camera):
    screen.fill(GROUND)

    # Ground grid
    grid_size = 80
    start_x = int(camera.x // grid_size) * grid_size
    start_y = int(camera.y // grid_size) * grid_size

    for x in range(start_x - 700, start_x + 700, grid_size):
        for y in range(start_y - 500, start_y + 500, grid_size):
            sx, sy = world_to_screen(x, y, camera)

            if -grid_size < sx < WIDTH and -grid_size < sy < HEIGHT:
                pygame.draw.rect(
                    screen, GROUND_LIGHT,
                    (sx, sy, grid_size - 2, grid_size - 2), 1
                )

    # Ground cracks
    for x, y, size_val in objects:
        sx, sy = world_to_screen(x, y, camera)

        if 0 < sx < WIDTH and 60 < sy < HEIGHT:
            pygame.draw.line(
                screen, GROUND_DARK, (sx, sy),
                (sx + size_val * 4, sy + size_val * 2), 2
            )

    # Buildings
    for x, y, w, h, shop in BUILDINGS:
        draw_building(screen, x, y, w, h, camera, shop)

    # Fountain
    fx, fy = world_to_screen(0, 0, camera)

    circles = [
        (GROUND_DARK, 76),
        ((45, 48, 55), 72),
        ((70, 75, 85), 63),
        (FOUNTAIN, 52),
        (WATER, 40)
    ]

    for color, radius in circles:
        pygame.draw.circle(screen, color, (fx, fy), radius)

    pygame.draw.circle(screen, BLUE, (fx, fy), 20, 3)
    pygame.draw.circle(screen, LIGHT, (fx, fy - 8), 8)

    # Cars
    for x, y, direction in CARS:
        draw_car(screen, x, y, direction, camera)

    # Street lamps
    lamps = [
        (-480, -350), (480, -350),
        (-480, 350), (480, 350),
        (-300, -450), (300, -450),
        (-300, 450), (300, 450)
    ]

    for x, y in lamps:
        sx, sy = world_to_screen(x, y, camera)

        if -30 < sx < WIDTH + 30 and -30 < sy < HEIGHT + 30:
            pygame.draw.circle(screen, (50, 55, 65), (sx, sy), 18)
            pygame.draw.circle(screen, LIGHT, (sx, sy), 6)
            pygame.draw.circle(screen, BLUE, (sx, sy), 2)

    # Boxes
    for x, y in PROPS:
        sx, sy = world_to_screen(x, y, camera)

        if -30 < sx < WIDTH + 30 and -30 < sy < HEIGHT + 30:
            pygame.draw.rect(screen, WOOD, (sx - 10, sy - 10, 20, 20))
            pygame.draw.line(screen, (40, 30, 25),
                             (sx - 9, sy - 9), (sx + 9, sy + 9), 2)
            pygame.draw.line(screen, (40, 30, 25),
                             (sx + 9, sy - 9), (sx - 9, sy + 9), 2)

    # Industrial pipes / barrels
    bushes = [
        (-680, -470), (650, -470),
        (-680, 450), (650, 450)
    ]

    for x, y in bushes:
        sx, sy = world_to_screen(x, y, camera)

        if -30 < sx < WIDTH + 30 and -30 < sy < HEIGHT + 30:
            pygame.draw.circle(screen, (55, 65, 60), (sx, sy), 20)
            pygame.draw.circle(screen, (35, 45, 40), (sx - 5, sy - 4), 12)


# INVISIBLE WALLS / COLLISION AREAS
def get_obstacles():
    obstacles = []

    # Buildings: invisible wall around each building
    for x, y, w, h, shop in BUILDINGS:
        obstacles.append(pygame.Rect(x, y, w, h))

    # Fountain
    obstacles.append(pygame.Rect(-70, -70, 140, 140))

    # Cars
    for x, y, direction in CARS:
        if direction == 0:
            obstacles.append(pygame.Rect(x - 20, y - 32, 40, 64))
        else:
            obstacles.append(pygame.Rect(x - 32, y - 20, 64, 40))

    # Boxes
    for x, y in PROPS:
        obstacles.append(pygame.Rect(x - 10, y - 10, 20, 20))

    return obstacles


# Move without passing through invisible walls
def move_player(player, dx, dy, obstacles):
    # Horizontal movement
    player.x += round(dx)

    for obj in obstacles:
        if player.colliderect(obj):
            if dx > 0:
                player.right = obj.left
            elif dx < 0:
                player.left = obj.right

    # Vertical movement
    player.y += round(dy)

    for obj in obstacles:
        if player.colliderect(obj):
            if dy > 0:
                player.bottom = obj.top
            elif dy < 0:
                player.top = obj.bottom

    return player


# Game setup
camera = Camera()
ground_objects = make_forest()
obstacles = get_obstacles()

# Player rectangle in world coordinates
player = pygame.Rect(-20, 100, 30, 40)

PLAYER_SPEED = 4
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += PLAYER_SPEED
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy -= PLAYER_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += PLAYER_SPEED

    # Prevent faster diagonal movement
    if dx != 0 and dy != 0:
        dx *= 0.7071
        dy *= 0.7071

    player = move_player(player, dx, dy, obstacles)

    # Camera follows player
    camera.update(player.centerx, player.centery)

    # Draw map
    draw_map(screen, ground_objects, camera)

    # Draw player
    px, py = world_to_screen(player.centerx, player.centery, camera)
    pygame.draw.ellipse(
        screen, PLAYER_COLOR,
        (px - player.width // 2, py - player.height // 2,
         player.width, player.height)
    )

    pygame.display.flip()

pygame.quit()
sys.exit()
