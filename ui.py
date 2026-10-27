import pygame

from settings import (
    WIDTH, HEIGHT, WHITE, RED, BLACK
)


def draw_text(screen, text, font, color, position):
    image = font.render(text, True, color)
    screen.blit(image, image.get_rect(center=position))


def make_button(screen, text, y, font, height=70):
    button = pygame.Rect(WIDTH // 2 - 130, y, 260, height)

    pygame.draw.rect(screen, RED, button)
    pygame.draw.rect(screen, WHITE, button, 2)
    draw_text(screen, text, font, WHITE, button.center)

    return button


def menu(screen, fonts):
    screen.fill(BLACK)

    draw_text(
        screen, "DEAD WOODS", fonts["big"],
        WHITE, (WIDTH // 2, 190)
    )
    draw_text(
        screen, "Survive 10 rounds in the forest",
        fonts["normal"], (175, 180, 165),
        (WIDTH // 2, 255)
    )

    button = make_button(
        screen, "START GAME", 330, fonts["normal"], 75
    )

    draw_text(
        screen,
        "WASD = Move   Mouse = Aim   Left Click = Shoot",
        fonts["small"], WHITE, (WIDTH // 2, 470)
    )

    return button


def end_screen(screen, fonts, health):
    screen.fill(BLACK)

    title = "YOU DIED" if health <= 0 else "YOU SURVIVED!"
    color = RED if health <= 0 else WHITE

    draw_text(
        screen, title, fonts["big"], color,
        (WIDTH // 2, 220)
    )

    return make_button(
        screen, "PLAY AGAIN", 320, fonts["normal"]
    )


def draw_game_ui(screen, fonts, health, round_no, zombie_count):
    pygame.draw.rect(screen, BLACK, (15, 15, 205, 35))
    pygame.draw.rect(
        screen, RED, (18, 18, max(0, int(health * 2)), 29)
    )

    screen.blit(
        fonts["small"].render(f"HP: {int(health)}", True, WHITE),
        (25, 21)
    )
    screen.blit(
        fonts["normal"].render(
            f"Round: {round_no}/10", True, WHITE
        ),
        (WIDTH - 190, 18)
    )
    screen.blit(
        fonts["small"].render(
            f"Zombies: {zombie_count}", True, WHITE
        ),
        (WIDTH - 190, 52)
    )