import pygame

from settings import WIDTH, HEIGHT, YELLOW


def shoot(player, mouse_pos, bullets, shoot_channel, shoot_sound):
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    direction = pygame.Vector2(mouse_pos) - center

    if direction.length_squared() == 0:
        return

    direction = direction.normalize()

    bullets.append({
        "pos": player + direction * 35,
        "vel": direction * 12,
    })

    shoot_channel.play(shoot_sound)


def update_bullets(bullets, zombies, player):
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


def draw_bullets(screen, bullets, camera):
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    for bullet in bullets:
        pos = bullet["pos"] - camera + center

        if screen.get_rect().collidepoint(pos):
            pygame.draw.circle(
                screen, YELLOW,
                (int(pos.x), int(pos.y)), 4
            )