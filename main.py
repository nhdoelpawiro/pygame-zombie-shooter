
import pygame

from settings import WIDTH, HEIGHT, RED
from map import make_forest, draw_forest
from player import update_player, draw_player
from zombies import (
    load_zombie_images,
    new_zombie,
    start_round,
    update_zombies,
    draw_zombies,
)

pygame.init()

if not pygame.mixer.get_init():
    pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dead Woods")
clock = pygame.time.Clock()

WHITE = (235, 235, 225)
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
trees = make_forest()
zombie_images = load_zombie_images()

ak_img = pygame.image.load("./assets/ak47.png").convert_alpha()
ak_img = pygame.transform.scale(ak_img, (90, 60))

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

game_started = False
game_over = False
paused = False
running = True

start_button = None
menu_quit_button = None
resume_button = None
pause_restart_button = None
pause_quit_button = None
end_restart_button = None


def draw_text(text, text_font, color, position):
    image = text_font.render(text, True, color)
    screen.blit(image, image.get_rect(center=position))


def make_button(text, y, height=65):
    button = pygame.Rect(
        WIDTH // 2 - 130,
        y,
        260,
        height
    )

    pygame.draw.rect(screen, RED, button)
    pygame.draw.rect(screen, WHITE, button, 2)
    draw_text(text, font, WHITE, button.center)

    return button


def menu():
    screen.fill(BLACK)

    draw_text(
        "DEAD WOODS",
        big_font,
        WHITE,
        (WIDTH // 2, 170)
    )

    draw_text(
        "Survive 10 rounds in the forest",
        font,
        (175, 180, 165),
        (WIDTH // 2, 230)
    )

    start = make_button("START GAME", 290, 65)
    quit_button = make_button("QUIT", 380, 65)

    draw_text(
        "WASD = Move   Mouse = Aim   Left Click = Shoot",
        small_font,
        WHITE,
        (WIDTH // 2, 490)
    )

    return start, quit_button


def pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    screen.blit(overlay, (0, 0))

    draw_text(
        "PAUSED",
        big_font,
        WHITE,
        (WIDTH // 2, 165)
    )

    resume = make_button("RESUME", 235, 60)
    restart = make_button("RESTART", 315, 60)
    quit_button = make_button("QUIT", 395, 60)

    return resume, restart, quit_button


def end_screen():
    screen.fill(BLACK)

    if health <= 0:
        title = "YOU DIED"
        color = RED
    else:
        title = "YOU SURVIVED!"
        color = WHITE

    draw_text(
        title,
        big_font,
        color,
        (WIDTH // 2, 220)
    )

    return make_button("PLAY AGAIN", 320, 70)


def stop_game_sounds():
    music.stop()
    walk_channel.stop()
    shoot_channel.stop()

    for channel in zombie_channels:
        channel.stop()


def reset_game():
    global health, round_no, round_timer
    global shoot_timer, zombie_sound_timer
    global game_over, paused

    health = 100
    round_no = 1
    round_timer = 0
    shoot_timer = 0
    zombie_sound_timer = 120
    game_over = False
    paused = False

    player.update(0, 160)
    camera.update(player)

    bullets.clear()
    zombies.clear()
    trees.clear()
    trees.extend(make_forest())

    stop_game_sounds()
    menu_music.stop()
    music.play(-1)

    start_round(zombies, round_no)


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
            if bullet["pos"].distance_to(zombie["pos"]) < zombie["size"] + 5:
                bullets.remove(bullet)
                zombie["hp"] -= 1

                if zombie["hp"] <= 0:
                    zombies.remove(zombie)

                break


def draw_bullets():
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    for bullet in bullets:
        pos = bullet["pos"] - camera + center

        if screen.get_rect().collidepoint(pos):
            pygame.draw.circle(
                screen,
                YELLOW,
                (int(pos.x), int(pos.y)),
                4
            )


def draw_game_ui():
    pygame.draw.rect(screen, BLACK, (15, 15, 205, 35))

    pygame.draw.rect(
        screen,
        RED,
        (18, 18, max(0, health) * 2, 29)
    )

    screen.blit(
        small_font.render(f"HP: {int(health)}", True, WHITE),
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


menu_music.play(-1)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_started and not game_over:
                    paused = not paused

                    if paused:
                        walk_channel.stop()
                    elif not music.get_num_channels():
                        music.play(-1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_started:
                if start_button and start_button.collidepoint(event.pos):
                    game_started = True
                    reset_game()
                elif menu_quit_button and menu_quit_button.collidepoint(event.pos):
                    running = False

            elif game_over:
                if end_restart_button and end_restart_button.collidepoint(event.pos):
                    reset_game()

            elif paused:
                if resume_button and resume_button.collidepoint(event.pos):
                    paused = False
                elif pause_restart_button and pause_restart_button.collidepoint(event.pos):
                    reset_game()
                elif pause_quit_button and pause_quit_button.collidepoint(event.pos):
                    running = False

            elif shoot_timer <= 0:
                shoot()
                shoot_timer = 10

    if not running:
        break

    if not game_started:
        menu_music.stop()
        start_button, menu_quit_button = menu()
        pygame.display.flip()
        continue

    if game_over:
        stop_game_sounds()
        end_restart_button = end_screen()
        pygame.display.flip()
        continue

    if paused:
        resume_button, pause_restart_button, pause_quit_button = pause_menu()
        pygame.display.flip()
        continue

    update_player(player, speed, walk_channel, walk_sound)
    camera.update(player)

    update_bullets()

    health = update_zombies(zombies, player, health)

    shoot_timer = max(0, shoot_timer - 1)
    round_timer = max(0, round_timer - 1)

    if health <= 0:
        health = 0
        game_over = True

    elif not zombies and round_timer == 0:
        if round_no < 10:
            round_no += 1
            start_round(zombies, round_no)
            round_timer = 90
        else:
            game_over = True

    draw_forest(screen, trees, camera)
    draw_zombies(screen, zombies, zombie_images, camera)
    draw_bullets()
    draw_player(screen, ak_img)
    draw_game_ui()

    if round_timer > 0:
        draw_text(
            f"ROUND {round_no}",
            big_font,
            RED,
            (WIDTH // 2, HEIGHT // 2)
        )

    pygame.display.flip()

stop_game_sounds()
menu_music.stop()
pygame.quit()
