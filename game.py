import pygame
import random
from map import make_forest, draw_forest

pygame.init()

if not pygame.mixer.get_init():
    pygame.mixer.init()

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


def new_zombie():
    side = random.choice(["top", "bottom", "left", "right"])

    offsets = {
        "top": (random.randint(-700, 700), -600),
        "bottom": (random.randint(-700, 700), 600),
        "left": (-600, random.randint(-400, 400)),
        "right": (600, random.randint(-400, 400))
    }

    x, y = offsets[side]

    return {
        "pos": player + pygame.Vector2(x, y),
        "speed": random.uniform(0.7, 1.2),
        "hp": 2
    }


def play_zombie_sound():
    for channel in zombie_channels:
        if not channel.get_busy():
            channel.play(random.choice(zombie_sounds))
            return


def start_round():
    global round_timer, zombie_sound_timer

    zombies.clear()
    bullets.clear()

    for _ in range(10 + (round_no - 1) * 15):
        zombies.append(new_zombie())

    round_timer = 90
    zombie_sound_timer = 120


def update_zombies():
    global health, zombie_sound_timer

    for zombie in zombies:
        direction = player - zombie["pos"]

        if direction.length_squared() > 0:
            direction = direction.normalize()
            zombie["pos"] += direction * zombie["speed"]

        if zombie["pos"].distance_to(player) < 28:
            health = max(0, health - 1)
            zombie["pos"] -= direction * 8
            play_zombie_sound()

    if zombies:
        zombie_sound_timer -= 1

        if zombie_sound_timer <= 0:
            play_zombie_sound()
            zombie_sound_timer = random.randint(120, 300)


def draw_zombies():
    for zombie in zombies:
        pos = zombie["pos"] - camera + pygame.Vector2(
            WIDTH // 2, HEIGHT // 2
        )

        if not screen.get_rect().inflate(200, 200).collidepoint(pos):
            continue

        pygame.draw.circle(screen, (70, 75, 67), pos, 17)
        pygame.draw.rect(
            screen, (50, 53, 49),
            (pos.x - 13, pos.y + 9, 26, 25)
        )
        pygame.draw.circle(
            screen, (145, 155, 103),
            (int(pos.x), int(pos.y - 10)), 13
        )

        for eye_x in (-5, 5):
            pygame.draw.circle(
                screen, RED,
                (int(pos.x + eye_x), int(pos.y - 12)), 3
            )


def update_player():
    keys = pygame.key.get_pressed()

    movement = pygame.Vector2(
        int(keys[pygame.K_d]) - int(keys[pygame.K_a]),
        int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    )

    if movement.length_squared() > 0:
        movement = movement.normalize()
        player.x = max(-1000, min(1000, player.x + movement.x * speed))
        player.y = max(-800, min(800, player.y + movement.y * speed))

        if not walk_channel.get_busy():
            walk_channel.play(walk_sound, -1)
    else:
        walk_channel.stop()

    camera.update(player)


def draw_player():
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    direction = pygame.Vector2(pygame.mouse.get_pos()) - center

    if direction.length_squared() > 0:
        direction = direction.normalize()
    else:
        direction = pygame.Vector2(1, 0)

    pygame.draw.circle(screen, (55, 57, 60), center, 18)
    pygame.draw.rect(
        screen, (45, 45, 48),
        (center.x - 14, center.y + 8, 28, 25)
    )
    pygame.draw.circle(
        screen, (206, 166, 128),
        center + direction * 4, 12
    )
    pygame.draw.line(
        screen, (30, 30, 30),
        center - direction * 15,
        center + direction * 42, 7
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