import pygame
from settings import WIDTH, HEIGHT, FPS, RED
from map import make_forest, draw_forest
from audio import load_audio
from player import update_player, draw_player
from zombies import (
    load_zombie_images,
    start_round,
    update_zombies,
    draw_zombies,
)
from weapons import shoot, update_bullets, draw_bullets
from ui import menu, end_screen, draw_text, draw_game_uisa

pygame.init()

if not pygame.mixer.get_init():
    pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dead Woods")
clock = pygame.time.Clock()

fonts = {
    "normal": pygame.font.Font(None, 36),
    "big": pygame.font.Font(None, 90),
    "small": pygame.font.Font(None, 24),
}

ak_img = pygame.image.load(
    "assets/ak47.png"
).convert_alpha()

ak_img = pygame.transform.scale(ak_img, (90, 60))

zombie_images = load_zombie_images()

audio = load_audio()
audio["menu_music"].play(-1)

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

game_started = False
game_over = False

start_button = None
restart_button = None

def reset_game():
    global health, round_no, round_timer
    global shoot_timer, zombie_sound_timer, game_over

    health = 100
    round_no = 1
    round_timer = 0
    shoot_timer = 0
    zombie_sound_timer = 120
    game_over = False

    player.update(0, 160)
    camera.update(player)

    bullets.clear()
    zombies.clear()

    trees.clear()
    trees.extend(make_forest())

    audio["walk_channel"].stop()
    audio["shoot_channel"].stop()

    for channel in audio["zombie_channels"]:
        channel.stop()

    audio["menu_music"].stop()
    audio["music"].stop()
    audio["music"].play(-1)

    start_round(zombies, round_no)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if not game_started and start_button:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    reset_game()
            elif game_over and restart_button:
                if restart_button.collidepoint(event.pos):
                    reset_game()
            elif game_started and not game_over:
                if shoot_timer <= 0:
                    shoot(
                        player,
                        pygame.mouse.get_pos(),
                        bullets,
                        audio["shoot_channel"],
                        audio["shoot"],
                    )
                    shoot_timer = 10

    if not game_started:
        start_button = menu(screen, fonts)
        pygame.display.flip()
        continue

    if game_over:
        restart_button = end_screen(
            screen,
            fonts,
            health,
        )

        pygame.display.flip()
        continue

    update_player(
        player,
        speed,
        audio["walk_channel"],
        audio["walk"],
    )

    camera.update(player)

    update_bullets(
        bullets,
        zombies,
        player,
    )

    health = update_zombies(
        zombies,
        player,
        health,
    )

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

    if game_over:
        audio["music"].stop()
        audio["walk_channel"].stop()

        for channel in audio["zombie_channels"]:
            channel.stop()

    draw_forest(screen, trees, camera)

    draw_zombies(
        screen,
        zombies,
        zombie_images,
        camera,
    )

    draw_bullets(
        screen,
        bullets,
        camera,
    )

    draw_player(
        screen,
        ak_img,
    )

    draw_game_ui(
        screen,
        fonts,
        health,
        round_no,
        len(zombies),
    )

    if round_timer > 0:
        draw_text(
            screen,
            f"ROUND {round_no}",
            fonts["big"],
            RED,
            (WIDTH // 2, HEIGHT // 2),
        )

    pygame.display.flip()

audio["music"].stop()
audio["menu_music"].stop()
audio["walk_channel"].stop()
audio["shoot_channel"].stop()

for channel in audio["zombie_channels"]:
    channel.stop()

pygame.quit()
