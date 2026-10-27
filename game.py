import pygame
import random
from map import make_forest, draw_forest


WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dead Woods")
clock = pygame.time.Clock()


def remove_background(image):
    image = image.convert_alpha()

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, a = image.get_at((x, y))

            # Zwarte achtergrond verwijderen
            if r < 30 and g < 30 and b < 30:
                image.set_at((x, y), (r, g, b, 0))

            # Witte watermerken en witte achtergrond verwijderen
            elif r > 235 and g > 235 and b > 235:
                image.set_at((x, y), (r, g, b, 0))

    return image

zombie_image = pygame.image.load("zombie_image.jpeg").convert()
zombie_image = pygame.transform.scale(zombie_image, (75, 95))
zombie_image = remove_background(zombie_image)

zombie_image = remove_background(zombie_image)

snelle_image = pygame.image.load("snelle_image.png").convert()
snelle_image = pygame.transform.scale(snelle_image, (60, 75))
snelle_image = remove_background(snelle_image)

tank_image = pygame.image.load("tank_image.webp").convert()
tank_image = pygame.transform.scale(tank_image, (90, 105))
tank_image = remove_background(tank_image)

boss_image = pygame.image.load("boss_image.png").convert()
boss_image = pygame.transform.scale(boss_image, (100, 120))
boss_image = remove_background(boss_image)




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

player = pygame.Vector2(0, 160)
camera = pygame.Vector2(0, 160)

speed = 4
health = 100
round_no = 1
round_timer = 0
shoot_timer = 0
zombie_sound_timer = 120

zombies = []
bullets = []
trees = []

game_started = False
game_over = False

music = pygame.mixer.Sound("./sfx/banditradio.mp3")
menu_music = pygame.mixer.Sound("./sfx/menu.mp3")
shoot_sound = pygame.mixer.Sound("./sfx/shoot.mp3")
walk_sound = pygame.mixer.Sound("./sfx/walk.mp3")

zombie_sounds = [
    pygame.mixer.Sound(f"./sfx/zombie{i}.mp3")
    for i in range(1, 5)
]

music.set_volume(0.5)
menu_music.set_volume(0.4)
shoot_sound.set_volume(0.7)
walk_sound.set_volume(0.7)

for sound in zombie_sounds:
    sound.set_volume(0.8)

walk_channel = pygame.mixer.Channel(1)
shoot_channel = pygame.mixer.Channel(2)
zombie_channels = [
    pygame.mixer.Channel(i) for i in range(3, 7)
]

menu_music.play(-1)


def new_zombie(zombie_type="normal"):
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        pos = (random.randint(0, W), -30)
    elif side == "bottom":
        pos = (random.randint(0, W), H + 30)
    elif side == "left":
        pos = (-30, random.randint(70, H))
    else:
        pos = (W + 30, random.randint(70, H))

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
            "max_hp": 12,
            "hp": 12,
            "type": "tank",
            "size": 20
        }

    # Boss zombie
    elif zombie_type == "boss":
        return {
            "pos": pygame.Vector2(pos),
            "speed": 0.5,
            "max_hp": 20,
            "hp": 20,
            "type": "boss",
            "size": 30
        }





def start_round():
    global round_no, round_timer

    round_timer = 90

    amount = 10 + (round_no - 1) * 5

    for _ in range(amount):
        chance = random.random()

        # Ronde 1-2: alleen normale zombies
        if round_no <= 2:
            zombie_type = "normal"

        # Ronde 3-4: snelle zombies worden geïntroduceerd
        elif round_no <= 4:
            if chance < 0.20:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        # Ronde 5-6: tank-zombies komen erbij
        elif round_no <= 6:
            if chance < 0.15:
                zombie_type = "tank"
            elif chance < 0.35:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        # Ronde 7-8: meer sterke zombies
        elif round_no <= 8:
            if chance < 0.10:
                zombie_type = "tank"
            elif chance < 0.35:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        # Ronde 9-10: boss-zombies verschijnen
        else:
            if chance < 0.10:
                zombie_type = "boss"
            elif chance < 0.25:
                zombie_type = "tank"
            elif chance < 0.50:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        zombies.append(new_zombie(zombie_type))



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
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    direction = pygame.Vector2(pygame.mouse.get_pos()) - center

    if direction.length_squared() > 0:
        direction = direction.normalize()
    else:
        direction = pygame.Vector2(1, 0)

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
    time = pygame.time.get_ticks()

    for z in zombies:
        p = z["pos"]
        size = z["size"]

        # Kies de juiste afbeelding
        if z["type"] == "normal":
            image = zombie_image
        elif z["type"] == "fast":
            image = snelle_image
        elif z["type"] == "tank":
            image = tank_image
        elif z["type"] == "boss":
            image = boss_image

        # Loopanimatie: op en neer bewegen
        bob = math.sin(time * 0.012 * (z["speed"] + 1)) * 4

        # Een kleine kantelbeweging tijdens het lopen
        angle = math.sin(time * 0.008 * (z["speed"] + 1)) * 8

        # Draai de afbeelding een beetje
        rotated_image = pygame.transform.rotate(image, angle)

        # Teken de zombie
        rect = rotated_image.get_rect(
            center=(int(p.x), int(p.y + bob))
        )
        screen.blit(rotated_image, rect)

        # HP-balk
        bar_width = size * 2
        hp_ratio = max(0, z["hp"] / z["max_hp"])

        pygame.draw.rect(
            screen, RED,
            (int(p.x - size), int(p.y - size - 8),
             bar_width, 4)
        )

        pygame.draw.rect(
            screen, (0, 255, 0),
            (int(p.x - size), int(p.y - size - 8),
             int(bar_width * hp_ratio), 4)
        )



def shoot():
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    direction = pygame.Vector2(pygame.mouse.get_pos()) - center

    if direction.length_squared() == 0:
        return

    direction = direction.normalize()

    bullets.append({
        "pos": player + direction * 35,
        "vel": direction * 12
    })

    shoot_channel.play(shoot_sound)


def update_bullets():
    for bullet in bullets[:]:
        bullet["pos"] += bullet["vel"]

        if bullet["pos"].distance_to(player) > 1200:
            bullets.remove(bullet)
            continue

        for zombie in zombies[:]:
            if bullet["pos"].distance_to(zombie["pos"]) < 20:
                bullets.remove(bullet)
                zombie["hp"] -= 1

                if zombie["hp"] <= 0:
                    zombies.remove(zombie)

                break


def draw_bullets():
    for bullet in bullets:
        pos = bullet["pos"] - camera + pygame.Vector2(
            WIDTH // 2, HEIGHT // 2
        )

        if screen.get_rect().collidepoint(pos):
            pygame.draw.circle(
                screen, YELLOW,
                (int(pos.x), int(pos.y)), 4
            )


def draw_text(text, text_font, color, position):
    image = text_font.render(text, True, color)
    screen.blit(image, image.get_rect(center=position))


def draw_game_ui():
    pygame.draw.rect(screen, BLACK, (15, 15, 205, 35))
    pygame.draw.rect(
        screen, RED, (18, 18, health * 2, 29)
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


def make_button(text, y, height=70):
    button = pygame.Rect(
        WIDTH // 2 - 130, y, 260, height
    )

    pygame.draw.rect(screen, RED, button)
    pygame.draw.rect(screen, WHITE, button, 2)
    draw_text(text, font, WHITE, button.center)

    return button


def menu():
    screen.fill(BLACK)

    draw_text("DEAD WOODS", big_font, WHITE, (WIDTH // 2, 190))
    draw_text(
        "Survive 10 rounds in the forest",
        font, (175, 180, 165), (WIDTH // 2, 255)
    )

    button = make_button("START GAME", 330, 75)

    draw_text(
        "WASD = Move   Mouse = Aim   Left Click = Shoot",
        small_font, WHITE, (WIDTH // 2, 470)
    )

    return button


def end_screen():
    screen.fill(BLACK)

    title = "YOU DIED" if health <= 0 else "YOU SURVIVED!"
    color = RED if health <= 0 else WHITE

    draw_text(title, big_font, color, (WIDTH // 2, 220))

    return make_button("PLAY AGAIN", 320)


def reset_game():
    global health, round_no, game_over
    global shoot_timer, zombie_sound_timer

    health = 100
    round_no = 1
    game_over = False
    shoot_timer = 0

    player.update(0, 160)
    camera.update(player)

    bullets.clear()
    zombies.clear()
    trees.clear()
    trees.extend(make_forest())

    for channel in zombie_channels:
        channel.stop()

    walk_channel.stop()
    music.stop()
    menu_music.stop()
    music.play(-1)

    start_round()


trees.extend(make_forest())

start_button = None
restart_button = None
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_started and start_button:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    reset_game()

            elif game_over and restart_button:
                if restart_button.collidepoint(event.pos):
                    reset_game()

            elif game_started and not game_over:
                if shoot_timer <= 0:
                    shoot()
                    shoot_timer = 10

    if not game_started:
        start_button = menu()
        pygame.display.flip()
        continue

    if game_over:
        restart_button = end_screen()
        pygame.display.flip()
        continue

    update_player()
    update_bullets()
    update_zombies()

    shoot_timer = max(0, shoot_timer - 1)
    round_timer = max(0, round_timer - 1)

    if health <= 0:
        game_over = True

    elif not zombies and round_timer == 0:
        if round_no < 10:
            round_no += 1
            start_round()
        else:
            game_over = True

    if game_over:
        music.stop()
        walk_channel.stop()

        for channel in zombie_channels:
            channel.stop()

    draw_forest(screen, trees, camera)
    draw_zombies()
    draw_bullets()
    draw_player()
    draw_game_ui()

    if round_timer > 0:
        draw_text(
            f"ROUND {round_no}",
            big_font, RED, (WIDTH // 2, HEIGHT // 2)
        )

    pygame.display.flip()

pygame.quit()