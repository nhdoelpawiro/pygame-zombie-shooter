
import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dead Woods - Zaun")
clock = pygame.time.Clock()

WHITE = (235, 235, 225)
RED = (190, 45, 45)
BLACK = (20, 20, 20)
YELLOW = (235, 205, 70)

# Map colors
GROUND = (25, 27, 33)
GROUND_LIGHT = (40, 44, 52)
GROUND_DARK = (15, 17, 21)
BUILDING = (42, 38, 52)
ROOF = (30, 27, 38)
WALL = (65, 55, 75)
WINDOW = (255, 170, 60)
NEON = (180, 40, 130)
BLUE = (0, 200, 220)
WOOD = (70, 50, 40)
FOUNTAIN = (50, 60, 70)
WATER = (30, 140, 160)
LIGHT = (255, 210, 120)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 90)
small_font = pygame.font.Font(None, 24)

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

LAMPS = [
    (-480, -350), (480, -350),
    (-480, 350), (480, 350),
    (-300, -450), (300, -450),
    (-300, 450), (300, 450)
]

BARRELS = [
    (-680, -470), (650, -470),
    (-680, 450), (650, 450)
]


# CAMERA
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 160

    def update(self, target):
        self.x += (target.x - self.x) * 0.1
        self.y += (target.y - self.y) * 0.1


def world_to_screen(x, y, camera):
    return (
        int(x - camera.x + WIDTH // 2),
        int(y - camera.y + HEIGHT // 2)
    )


# GROUND DETAILS
def make_forest():
    objects = []
    random.seed(10)

    for i in range(100):
        x = random.randint(-950, 950)
        y = random.randint(-750, 750)

        if not (-170 < x < 170 and -130 < y < 130):
            objects.append((x, y, random.randint(1, 3)))

    return objects


# CARS
def draw_car(x, y, direction, camera):
    sx, sy = world_to_screen(x, y, camera)
    car = pygame.Surface((40, 64), pygame.SRCALPHA)

    pygame.draw.rect(
        car, (10, 10, 12, 140),
        (5, 5, 32, 54), border_radius=10
    )

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

    pygame.draw.polygon(
        car, (20, 25, 35),
        [(10, 21), (30, 21), (28, 31), (12, 31)]
    )

    pygame.draw.polygon(
        car, (20, 25, 35),
        [(12, 35), (28, 35), (30, 44), (10, 44)]
    )

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


# BUILDINGS
def draw_building(x, y, w, h, camera, shop=False):
    sx, sy = world_to_screen(x, y, camera)

    if sx + w < -100 or sx > WIDTH + 100:
        return

    if sy + h < -100 or sy > HEIGHT + 100:
        return

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
        pygame.draw.rect(
            screen, NEON,
            (sx + 10, sy + h - 22, w - 20, 8),
            border_radius=3
        )

        pygame.draw.rect(
            screen, BLUE,
            (sx + 15, sy + h - 14, w - 30, 3)
        )


# MAP
def draw_forest(screen, objects, camera):
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
                screen, GROUND_DARK,
                (sx, sy),
                (sx + size_val * 4, sy + size_val * 2),
                2
            )

    # Buildings
    for x, y, w, h, shop in BUILDINGS:
        draw_building(x, y, w, h, camera, shop)

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
        draw_car(x, y, direction, camera)

    # Street lamps
    for x, y in LAMPS:
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

            pygame.draw.line(
                screen, (40, 30, 25),
                (sx - 9, sy - 9), (sx + 9, sy + 9), 2
            )

            pygame.draw.line(
                screen, (40, 30, 25),
                (sx + 9, sy - 9), (sx - 9, sy + 9), 2
            )

    # Barrels
    for x, y in BARRELS:
        sx, sy = world_to_screen(x, y, camera)

        if -30 < sx < WIDTH + 30 and -30 < sy < HEIGHT + 30:
            pygame.draw.circle(screen, (55, 65, 60), (sx, sy), 20)
            pygame.draw.circle(screen, (35, 45, 40), (sx - 5, sy - 4), 12)


# INVISIBLE WALLS
def get_obstacles():
    obstacles = []

    # Buildings
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


# PLAYER MOVEMENT AND COLLISIONS
def move_player(player, movement, obstacles):
    player_rect = pygame.Rect(0, 0, 28, 38)
    player_rect.center = (round(player.x), round(player.y))

    # Horizontal movement
    player_rect.x += round(movement.x)

    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            if movement.x > 0:
                player_rect.right = obstacle.left
            elif movement.x < 0:
                player_rect.left = obstacle.right

    player.x = player_rect.centerx

    # Vertical movement
    player_rect.centerx = round(player.x)
    player_rect.y = round(player.y) - player_rect.height // 2
    player_rect.y += round(movement.y)

    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            if movement.y > 0:
                player_rect.bottom = obstacle.top
            elif movement.y < 0:
                player_rect.top = obstacle.bottom

    player.y = player_rect.centery

    # World boundaries
    player.x = max(-1100, min(1100, player.x))
    player.y = max(-850, min(850, player.y))


# ZOMBIES
def new_zombie():
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        x = player.x + random.randint(-700, 700)
        y = player.y - 600

    elif side == "bottom":
        x = player.x + random.randint(-700, 700)
        y = player.y + 600

    elif side == "left":
        x = player.x - 600
        y = player.y + random.randint(-400, 400)

    else:
        x = player.x + 600
        y = player.y + random.randint(-400, 400)

    return {
        "pos": pygame.Vector2(x, y),
        "speed": random.uniform(0.7, 1.2),
        "hp": 2
    }


def start_round():
    global round_timer

    zombies.clear()

    amount = 10 + (round_no - 1) * 15

    for i in range(amount):
        zombies.append(new_zombie())

    round_timer = 90


def update_zombies():
    global health

    for zombie in zombies:
        direction = player - zombie["pos"]

        if direction.length() > 0:
            direction.normalize_ip()
            zombie["pos"] += direction * zombie["speed"]

        if zombie["pos"].distance_to(player) < 28:
            health -= 1

            if direction.length() > 0:
                zombie["pos"] -= direction * 8


def draw_zombies():
    for zombie in zombies:
        pos = zombie["pos"] - pygame.Vector2(camera.x, camera.y)
        pos += pygame.Vector2(WIDTH // 2, HEIGHT // 2)

        if (
            pos.x < -100 or pos.x > WIDTH + 100
            or pos.y < -100 or pos.y > HEIGHT + 100
        ):
            continue

        pygame.draw.circle(
            screen, (70, 75, 67),
            (int(pos.x), int(pos.y)), 17
        )

        pygame.draw.rect(
            screen, (50, 53, 49),
            (pos.x - 13, pos.y + 9, 26, 25)
        )

        pygame.draw.circle(
            screen, (145, 155, 103),
            (int(pos.x), int(pos.y - 10)), 13
        )

        pygame.draw.circle(
            screen, RED,
            (int(pos.x - 5), int(pos.y - 12)), 3
        )

        pygame.draw.circle(
            screen, RED,
            (int(pos.x + 5), int(pos.y - 12)), 3
        )


# PLAYER
def update_player():
    keys = pygame.key.get_pressed()
    movement = pygame.Vector2()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        movement.y -= 1

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        movement.y += 1

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        movement.x -= 1

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        movement.x += 1

    if movement.length() > 0:
        movement.normalize_ip()
        movement *= speed
        move_player(player, movement, obstacles)

    camera.update(player)


def draw_player():
    mouse = pygame.Vector2(pygame.mouse.get_pos())
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    direction = mouse - center

    if direction.length() == 0:
        direction = pygame.Vector2(1, 0)

    direction.normalize_ip()

    # Body
    pygame.draw.circle(
        screen, (55, 57, 60),
        (int(center.x), int(center.y)), 18
    )

    pygame.draw.rect(
        screen, (45, 45, 48),
        (center.x - 14, center.y + 8, 28, 25)
    )

    # Head
    head = center + direction * 4

    pygame.draw.circle(
        screen, (206, 166, 128),
        (int(head.x), int(head.y)), 12
    )

    # Weapon follows mouse
    start = center + direction * 10
    end = center + direction * 42

    pygame.draw.line(
        screen, (30, 30, 30),
        (int(start.x), int(start.y)),
        (int(end.x), int(end.y)), 7
    )

    pygame.draw.line(
        screen, (100, 105, 110),
        (int(start.x), int(start.y)),
        (int(end.x), int(end.y)), 3
    )


# SHOOTING
def shoot():
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    direction = pygame.Vector2(
        pygame.mouse.get_pos()
    ) - center

    if direction.length() == 0:
        return

    direction.normalize_ip()

    bullets.append({
        "pos": player + direction * 35,
        "vel": direction * 12
    })


def update_bullets():
    for bullet in bullets[:]:
        bullet["pos"] += bullet["vel"]

        if bullet["pos"].distance_to(player) > 1200:
            bullets.remove(bullet)
            continue

        for zombie in zombies[:]:
            if bullet["pos"].distance_to(zombie["pos"]) < 20:
                zombie["hp"] -= 1

                if bullet in bullets:
                    bullets.remove(bullet)

                if zombie["hp"] <= 0:
                    zombies.remove(zombie)

                break


def draw_bullets():
    for bullet in bullets:
        pos = bullet["pos"] - pygame.Vector2(camera.x, camera.y)
        pos += pygame.Vector2(WIDTH // 2, HEIGHT // 2)

        if -10 < pos.x < WIDTH + 10 and -10 < pos.y < HEIGHT + 10:
            pygame.draw.circle(
                screen, YELLOW,
                (int(pos.x), int(pos.y)), 4
            )


# USER INTERFACE
def draw_game_ui():
    pygame.draw.rect(screen, BLACK, (15, 15, 205, 35))

    pygame.draw.rect(
        screen, RED,
        (18, 18, max(0, health) * 2, 29)
    )

    screen.blit(
        small_font.render(f"HP: {health}", True, WHITE),
        (25, 21)
    )

    screen.blit(
        font.render(f"Round: {round_no}/10", True, WHITE),
        (WIDTH - 190, 18)
    )

    screen.blit(
        small_font.render(f"Zombies: {len(zombies)}", True, WHITE),
        (WIDTH - 190, 52)
    )


def draw_round():
    if round_timer <= 0:
        return

    progress = 1 - round_timer / 90
    size = int(55 + progress * 35)

    round_font = pygame.font.Font(None, size)

    text = round_font.render(
        f"ROUND {round_no}", True, RED
    )

    screen.blit(
        text,
        text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    )


# START MENU
def menu():
    screen.fill(BLACK)

    title = big_font.render("DEAD WOODS", True, WHITE)

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 190))
    )

    subtitle = font.render(
        "Survive 10 rounds in Zaun",
        True, (175, 180, 165)
    )

    screen.blit(
        subtitle,
        subtitle.get_rect(center=(WIDTH // 2, 255))
    )

    button = pygame.Rect(
        WIDTH // 2 - 130, 330, 260, 75
    )

    pygame.draw.rect(screen, RED, button)
    pygame.draw.rect(screen, WHITE, button, 2)

    text = font.render("START GAME", True, WHITE)

    screen.blit(
        text,
        text.get_rect(center=button.center)
    )

    controls = small_font.render(
        "WASD / Arrows = Move   Mouse = Aim   Left Click = Shoot",
        True, WHITE
    )

    screen.blit(
        controls,
        controls.get_rect(center=(WIDTH // 2, 470))
    )

    return button


# GAME OVER
def end_screen():
    screen.fill(BLACK)

    if health <= 0:
        title = big_font.render("YOU DIED", True, RED)
    else:
        title = big_font.render("YOU SURVIVED!", True, WHITE)

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 220))
    )

    button = pygame.Rect(
        WIDTH // 2 - 130, 320, 260, 70
    )

    pygame.draw.rect(screen, RED, button)

    text = font.render("PLAY AGAIN", True, WHITE)

    screen.blit(
        text,
        text.get_rect(center=button.center)
    )

    return button


# RESET GAME
def reset_game():
    global health, round_no, game_over, shoot_timer

    health = 100
    round_no = 1
    game_over = False
    shoot_timer = 0

    player.update(0, 160)

    camera.x = 0
    camera.y = 160

    bullets.clear()
    trees.clear()
    trees.extend(make_forest())

    start_round()


# GAME SETTINGS
player = pygame.Vector2(0, 160)
camera = Camera()

speed = 4
health = 100
round_no = 1

zombies = []
bullets = []
trees = make_forest()

obstacles = get_obstacles()

round_timer = 0
shoot_timer = 0

game_started = False
game_over = False

running = True
start_button = None
restart_button = None


# MAIN GAME LOOP
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not game_started and start_button:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    reset_game()

            elif game_started and not game_over:
                if event.button == 1 and shoot_timer <= 0:
                    shoot()
                    shoot_timer = 10

            elif game_over and restart_button:
                if restart_button.collidepoint(event.pos):
                    reset_game()

    if not game_started:
        start_button = menu()
        pygame.display.flip()
        continue

    if game_over:
        restart_button = end_screen()
        pygame.display.flip()
        continue

    update_player()

    if shoot_timer > 0:
        shoot_timer -= 1

    update_bullets()
    update_zombies()

    if health <= 0:
        game_over = True

    if round_timer > 0:
        round_timer -= 1

    if not zombies and round_timer <= 0:
        if round_no < 10:
            round_no += 1
            start_round()
        else:
            game_over = True

    draw_forest(screen, trees, camera)
    draw_zombies()
    draw_bullets()
    draw_player()
    draw_game_ui()
    draw_round()

    pygame.display.flip()


pygame.quit()
sys.exit()
