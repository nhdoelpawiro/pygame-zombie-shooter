import pygame
import random
import math

pygame.init()
W, H = 1000, 650
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dead Woods")
clock = pygame.time.Clock()

# Colors
GREEN = (67, 72, 61)
DARK = (42, 48, 41)
TREE = (48, 68, 46)
TRUNK = (82, 62, 45)
WHITE = (235, 235, 225)
RED = (190, 45, 45)
BLACK = (20, 20, 20)
YELLOW = (235, 205, 70)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 90)
small_font = pygame.font.Font(None, 24)

player = pygame.Vector2(W // 2, H // 2)
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


def new_zombie():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        pos = (random.randint(0, W), -30)
    elif side == "bottom":
        pos = (random.randint(0, W), H + 30)
    elif side == "left":
        pos = (-30, random.randint(70, H))
    else:
        pos = (W + 30, random.randint(70, H))

    return {"pos": pygame.Vector2(pos),
            "speed": random.uniform(.7, 1.2),
            "hp": 2}


def start_round():
    global round_timer
    zombies.clear()
    amount = 10 + (round_no - 1) * 15
    for _ in range(amount):
        zombies.append(new_zombie())
    round_timer = 90


def draw_forest():
    screen.fill(GREEN)

    for i in range(35):
        x = (i * 83) % W
        y = 75 + (i * 137) % (H - 85)
        pygame.draw.circle(screen, DARK, (x, y), 3)

    for x, y in trees:
        pygame.draw.rect(screen, TRUNK, (x - 7, y + 10, 14, 35))
        pygame.draw.circle(screen, TREE, (x, y), 29)
        pygame.draw.circle(screen, TREE, (x - 10, y - 8), 22)
        pygame.draw.circle(screen, TREE, (x + 12, y - 5), 21)


def draw_player():
    mouse = pygame.Vector2(pygame.mouse.get_pos())
    direction = mouse - player
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
        pygame.draw.circle(screen, (70, 75, 67), p, 17)
        pygame.draw.rect(screen, (50, 53, 49),
                         (p.x - 13, p.y + 9, 26, 25))
        pygame.draw.circle(screen, (145, 155, 103),
                           (int(p.x), int(p.y - 10)), 13)
        pygame.draw.circle(screen, RED, (int(p.x - 5), int(p.y - 12)), 3)
        pygame.draw.circle(screen, RED, (int(p.x + 5), int(p.y - 12)), 3)


def shoot():
    direction = pygame.Vector2(pygame.mouse.get_pos()) - player
    if direction.length() == 0:
        return
    direction.normalize_ip()
    bullets.append({
        "pos": player + direction * 35,
        "vel": direction * 12
    })


def update_player():
    move = pygame.Vector2(0, 0)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        move.y -= 1
    if keys[pygame.K_s]:
        move.y += 1
    if keys[pygame.K_a]:
        move.x -= 1
    if keys[pygame.K_d]:
        move.x += 1

    if move.length() > 0:
        move.normalize_ip()
        player.x += move.x * speed
        player.y += move.y * speed

    player.x = max(25, min(W - 25, player.x))
    player.y = max(75, min(H - 25, player.y))


def update_bullets():
    for b in bullets[:]:
        b["pos"] += b["vel"]

        if not screen.get_rect().collidepoint(b["pos"]):
            bullets.remove(b)
            continue

        for z in zombies[:]:
            if b["pos"].distance_to(z["pos"]) < 20:
                z["hp"] -= 1
                bullets.remove(b)

                if z["hp"] <= 0:
                    zombies.remove(z)
                break


def update_zombies():
    global health

    for z in zombies:
        direction = player - z["pos"]

        if direction.length() > 0:
            direction.normalize_ip()
            z["pos"] += direction * z["speed"]

        if z["pos"].distance_to(player) < 28:
            health -= 1
            z["pos"] -= direction * 8


def draw_game_ui():
    pygame.draw.rect(screen, BLACK, (15, 15, 205, 35))
    pygame.draw.rect(screen, RED, (18, 18, max(0, health) * 2, 29))
    screen.blit(small_font.render(f"HP: {health}", True, WHITE), (25, 21))

    screen.blit(font.render(f"Round: {round_no}/10", True, WHITE),
                (W - 190, 18))
    screen.blit(small_font.render(f"Zombies: {len(zombies)}", True, WHITE),
                (W - 190, 52))


def draw_round():
    if round_timer <= 0:
        return

    progress = 1 - round_timer / 90
    size = int(55 + progress * 35)
    f = pygame.font.Font(None, size)
    text = f.render(f"ROUND {round_no}", True, RED)
    screen.blit(text, text.get_rect(center=(W // 2, H // 2)))


def menu():
    screen.fill(DARK)

    title = big_font.render("DEAD WOODS", True, WHITE)
    screen.blit(title, title.get_rect(center=(W // 2, 190)))

    sub = font.render("Survive 10 rounds in the forest",
                      True, (175, 180, 165))
    screen.blit(sub, sub.get_rect(center=(W // 2, 255)))

    button = pygame.Rect(W // 2 - 130, 330, 260, 75)
    pygame.draw.rect(screen, RED, button)
    pygame.draw.rect(screen, WHITE, button, 2)

    text = font.render("START GAME", True, WHITE)
    screen.blit(text, text.get_rect(center=button.center))

    controls = small_font.render(
        "WASD = Move   Mouse = Aim   Left Click = Shoot",
        True, WHITE)
    screen.blit(controls, controls.get_rect(center=(W // 2, 470)))
    return button


def end_screen():
    screen.fill(DARK)

    if health <= 0:
        title = big_font.render("YOU DIED", True, RED)
    else:
        title = big_font.render("YOU SURVIVED!", True, WHITE)

    screen.blit(title, title.get_rect(center=(W // 2, 220)))

    button = pygame.Rect(W // 2 - 130, 320, 260, 70)
    pygame.draw.rect(screen, RED, button)
    text = font.render("PLAY AGAIN", True, WHITE)
    screen.blit(text, text.get_rect(center=button.center))
    return button


def reset_game():
    global health, round_no, game_over, shoot_timer
    health = 100
    round_no = 1
    game_over = False
    shoot_timer = 0
    player.update(W // 2, H // 2)
    bullets.clear()
    make_forest()
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

    # When every zombie is dead, start the next round.
    if not zombies and round_timer <= 0:
        if round_no < 10:
            round_no += 1
            start_round()
        else:
            game_over = True

    draw_forest()
    draw_zombies()

    for b in bullets:
        pygame.draw.circle(screen, YELLOW,
                           (int(b["pos"].x), int(b["pos"].y)), 4)

    draw_player()
    draw_game_ui()
    draw_round()

    pygame.display.flip()

pygame.quit()
