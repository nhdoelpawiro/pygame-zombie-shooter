import pygame
import random
import math

from map import make_forest, draw_forest

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dead Woods")
clock = pygame.time.Clock()

WHITE = (235, 235, 225)
RED = (190, 45, 45)
BLACK = (20, 20, 20)
YELLOW = (235, 205, 70)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 90)
small_font = pygame.font.Font(None, 24)
player = pygame.Vector2(0, 160)
camera = pygame.Vector2(0, 160)

speed = 4
health = 100
round_no = 1

zombies = []
bullets = []
trees = []

round_timer = 0
shoot_timer = 0

game_started = False
game_over = False


def make_forest():
    trees.clear()
    while len(trees) < 25:
        x = random.randint(40, W - 40)
        y = random.randint(90, H - 40)
        if not (330 < x < 670 and 190 < y < 470):
            trees.append((x, y))


def new_zombie(zombie_type="normal"):
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

    # Normale zombie
    if zombie_type == "normal":
        return {
            "pos": pygame.Vector2(pos),
            "speed": random.uniform(0.7, 1.2),
            "max_hp": 2,
            "hp": 2,
            "type": "normal",
            "size": 15
        }

    # Snelle zombie
    elif zombie_type == "fast":
        return {
            "pos": pygame.Vector2(pos),
            "speed": random.uniform(2.0, 2.8),
            "max_hp": 1,
            "hp": 1,
            "type": "fast",
            "size": 12
        }

    # Tank zombie
    elif zombie_type == "tank":
        return {
            "pos": pygame.Vector2(pos),
            "speed": random.uniform(0.4, 0.7),
            "max_hp": 8,
            "hp": 8,
            "type": "tank",
            "size": 25
        }

    # Boss zombie
    elif zombie_type == "boss":
        return {
            "pos": pygame.Vector2(pos),
            "speed": 0.5,
            "max_hp": 20,
            "type": "boss",
            "size": 40
        }




def start_round():
    global round_no, round_timer

    round_no += 1
    round_timer = 90

    amount = 10 + (round_no - 1) * 15


    for _ in range(amount):
        chance = random.random()

        if round_no <= 2:
            zombie_type = "normal"

        elif round_no <= 4:
            zombie_type = "fast" if chance < 0.25 else "normal"

        elif round_no <= 7:
            if chance < 0.15:
                zombie_type = "tank"
            elif chance < 0.40:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        else:
            if chance < 0.05:
                zombie_type = "boss"
            elif chance < 0.20:
                zombie_type = "tank"
            elif chance < 0.45:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        zombies.append(new_zombie(zombie_type))

def update_zombies():
    global health

    for zombie in zombies:
        direction = player - zombie["pos"]

        if direction.length() > 0:
            direction.normalize_ip()
            zombie["pos"] += direction * zombie["speed"]

        # Zombie attacks player
        if zombie["pos"].distance_to(player) < 28:
            health -= 1
            zombie["pos"] -= direction * 8

def draw_zombies():
    for zombie in zombies:
        pos = zombie["pos"] - camera
        pos += pygame.Vector2(WIDTH // 2, HEIGHT // 2)

        # don't draw zombies outside of screen
        if (
            pos.x < -100
            or pos.x > WIDTH + 100
            or pos.y < -100
            or pos.y > HEIGHT + 100
        ):
            continue
        
        ## drawing the zombie
        pygame.draw.circle(
            screen,
            (70, 75, 67),
            pos,
            17
        )
        pygame.draw.rect(
            screen,
            (50, 53, 49),
            (pos.x - 13, pos.y + 9, 26, 25)
        )
        pygame.draw.circle(
            screen,
            (145, 155, 103),
            (int(pos.x), int(pos.y - 10)),
            13
        )
        pygame.draw.circle(
            screen,
            RED,
            (int(pos.x - 5), int(pos.y - 12)),
            3
        )
        pygame.draw.circle(
            screen,
            RED,
            (int(pos.x + 5), int(pos.y - 12)),
            3
        )

def update_player():
    global player

    keys = pygame.key.get_pressed()
    movement = pygame.Vector2()

    ## player movement
    if keys[pygame.K_w]:
        movement.y -= 1
    if keys[pygame.K_s]:
        movement.y += 1
    if keys[pygame.K_a]:
        movement.x -= 1
    if keys[pygame.K_d]:
        movement.x += 1
    if movement.length() > 0:
        movement.normalize_ip()
        player += movement * speed

    # Keep player inside map
    player.x = max(-1000, min(1000, player.x))
    player.y = max(-800, min(800, player.y))

    camera.update(player)

def draw_player():
    mouse = pygame.Vector2(pygame.mouse.get_pos())
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    direction = mouse - center

    if direction.length() == 0:
        direction = pygame.Vector2(1, 0)

    direction.normalize_ip()

    pygame.draw.circle(screen, (55, 57, 60), player, 18)
    pygame.draw.rect(screen, (45, 45, 48),
                     (player.x - 14, player.y + 8, 28, 25))

    head = player + direction * 4
    pygame.draw.circle(screen, (206, 166, 128), head, 12)
    pygame.draw.arc(screen, (70, 45, 35),
                    (head.x - 12, head.y - 13, 24, 22),
                    math.pi, math.pi * 2, 5)

    # Simple M4
    pygame.draw.line(screen, (30, 30, 30),
                     player - direction * 15,
                     player + direction * 42, 7)
    pygame.draw.line(screen, (80, 80, 78),
                     player + direction * 15,
                     player + direction * 34, 4)


def draw_zombies():
    for z in zombies:
        p = z["pos"]
        size = z["size"]

        if z["type"] == "normal":
            head_color = (145, 155, 103)
            body_color = (50, 53, 49)

        elif z["type"] == "fast":
            head_color = (220, 70, 70)
            body_color = (100, 35, 35)

        elif z["type"] == "tank":
            head_color = (75, 105, 75)
            body_color = (35, 45, 35)

        elif z["type"] == "boss":
            head_color = (150, 60, 170)
            body_color = (55, 20, 65)

        pygame.draw.circle(screen, body_color,
                           (int(p.x), int(p.y + size)), size)

        pygame.draw.circle(screen, head_color,
                           (int(p.x), int(p.y)), size)

        # Rode ogen
        pygame.draw.circle(screen, (255, 0, 0),
                           (int(p.x - size // 3), int(p.y - size // 4)), 3)

        pygame.draw.circle(screen, (255, 0, 0),
                           (int(p.x + size // 3), int(p.y - size // 4)), 3)

        # HP-balk
        bar_width = size * 2
        hp_ratio = z["hp"] / z["max_hp"]

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (int(p.x - size), int(p.y - size - 8),
             bar_width, 4)
        )

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (int(p.x - size), int(p.y - size - 8),
             int(bar_width * hp_ratio), 4)
        )


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

        # remove bullets that go too far
        if bullet["pos"].distance_to(player) > 1200:
            bullets.remove(bullet)
            continue

        # zombie collision check
        for zombie in zombies[:]:
            if bullet["pos"].distance_to(zombie["pos"]) < 20:
                zombie["hp"] -= 1

                bullets.remove(bullet)

                if zombie["hp"] <= 0:
                    zombies.remove(zombie)

                break

def draw_bullets():
    for bullet in bullets:
        pos = bullet["pos"] - camera
        pos += pygame.Vector2(WIDTH // 2, HEIGHT // 2)

        if (
            -10 < pos.x < WIDTH + 10
            and -10 < pos.y < HEIGHT + 10
        ):
            pygame.draw.circle(
                screen,
                YELLOW,
                (int(pos.x), int(pos.y)),
                4
            )

def draw_game_ui():
    
    # health bar
    pygame.draw.rect(
        screen,
        BLACK,
        (15, 15, 205, 35)
    )
    pygame.draw.rect(
        screen,
        RED,
        (
            18,
            18,
            max(0, health) * 2,
            29
        )
    )

    screen.blit(
        small_font.render(
            f"HP: {health}",
            True,
            WHITE
        ),
        (25, 21)
    )

    screen.blit(
        font.render(
            f"Round: {round_no}/10",
            True,
            WHITE
        ),
        (WIDTH - 190, 18)
    )

    screen.blit(
        small_font.render(
            f"Zombies: {len(zombies)}",
            True,
            WHITE
        ),
        (WIDTH - 190, 52)
    )

def draw_round():
    if round_timer <= 0:
        return

    progress = 1 - round_timer / 90
    size = int(55 + progress * 35)

    round_font = pygame.font.Font(None, size)

    text = round_font.render(
        f"ROUND {round_no}",
        True,
        RED
    )

    screen.blit(
        text,
        text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )
    )

def menu():
    screen.fill(BLACK)

    title = big_font.render(
        "DEAD WOODS",
        True,
        WHITE
    )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, 190)
        )
    )

    subtitle = font.render(
        "Survive 10 rounds in the forest",
        True,
        (175, 180, 165)
    )

    screen.blit(
        subtitle,
        subtitle.get_rect(
            center=(WIDTH // 2, 255)
        )
    )

    button = pygame.Rect(
        WIDTH // 2 - 130,
        330,
        260,
        75
    )

    pygame.draw.rect(
        screen,
        RED,
        button
    )

    pygame.draw.rect(
        screen,
        WHITE,
        button,
        2
    )

    text = font.render(
        "START GAME",
        True,
        WHITE
    )

    screen.blit(
        text,
        text.get_rect(
            center=button.center
        )
    )

    controls = small_font.render(
        "WASD = Move   Mouse = Aim   Left Click = Shoot",
        True,
        WHITE
    )

    screen.blit(
        controls,
        controls.get_rect(
            center=(WIDTH // 2, 470)
        )
    )

    return button

def end_screen():
    screen.fill(BLACK)

    if health <= 0:
        title = big_font.render(
            "YOU DIED",
            True,
            RED
        )
    else:
        title = big_font.render(
            "YOU SURVIVED!",
            True,
            WHITE
        )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, 220)
        )
    )

    button = pygame.Rect(
        WIDTH // 2 - 130,
        320,
        260,
        70
    )

    pygame.draw.rect(
        screen,
        RED,
        button
    )

    text = font.render(
        "PLAY AGAIN",
        True,
        WHITE
    )

    screen.blit(
        text,
        text.get_rect(
            center=button.center
        )
    )

    return button

def reset_game():
    global health, round_no
    global game_over, shoot_timer

    health = 100
    round_no = 1
    game_over = False
    shoot_timer = 0

    player.update(0, 160)
    camera.update(player)

    bullets.clear()
    trees.clear()
    trees.extend(make_forest())
    start_round()

running = True
start_button = None
restart_button = None

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