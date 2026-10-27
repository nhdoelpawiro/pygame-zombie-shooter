import pygame

from settings import WIDTH, HEIGHT


def update_player(player, speed, walk_channel, walk_sound):
    keys = pygame.key.get_pressed()

    movement = pygame.Vector2(
        int(keys[pygame.K_d]) - int(keys[pygame.K_a]),
        int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    )

    if movement.length_squared() > 0:
        movement = movement.normalize()

        player.x = max(
            -1000,
            min(1000, player.x + movement.x * speed)
        )

        player.y = max(
            -800,
            min(800, player.y + movement.y * speed)
        )

        if not walk_channel.get_busy():
            walk_channel.play(walk_sound, -1)
    else:
        walk_channel.stop()

    return player


def draw_player(screen, ak_img):
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    mouse = pygame.Vector2(pygame.mouse.get_pos())
    direction = mouse - center

    if direction.length_squared() > 0:
        direction = direction.normalize()
    else:
        direction = pygame.Vector2(1, 0)

    pixel = 2
    ox, oy = int(center.x), int(center.y)

    BLACK = (10, 10, 12)
    HAIR = (25, 20, 35)
    SKIN = (230, 175, 145)
    SCARF = (130, 50, 110)
    SHIRT = (25, 25, 30)
    PANTS = (190, 190, 195)
    BELT = (20, 20, 25)

    sprite = [
        ".......HHH........",
        "......HHHHH.......",
        ".....HHHHHHH......",
        "....HHHHHHHHH.....",
        "...HHHHHHHHHHH....",
        "...HHHHSSSSHHH....",
        "...HHHSSSSSSHH....",
        "....HHSSSSSSHH....",
        "....HSSSSSSSSH....",
        ".....SSSSSSSS.....",
        "....PPSSSSSSPP....",
        "...PPPCCCCCCPPP...",
        "...PPCCCCCCCCPP...",
        "...PCCCCCCCCCCP...",
        "....CCCCCCCCCC....",
        "....CCccccccCC....",
        "......sssssss.....",
        ".....ssssssss.....",
        ".....sssssssss....",
        ".....WWWWWWWWWW...",
        "....WWWWWWWWWW....",
        "....WWWBBBBWWW....",
        "....WWWW..WWWW....",
        "....WWW....WWW....",
        "....WW......WW....",
        "....WW......WW....",
        "....BB......BB....",
        "....BB......BB....",
    ]

    colors = {
        "H": HAIR,
        "S": SKIN,
        "s": SKIN,
        "P": SCARF,
        "C": SHIRT,
        "c": SHIRT,
        "W": PANTS,
        "w": PANTS,
        "B": BELT,
    }

    for y, row in enumerate(sprite):
        for x, char in enumerate(row):
            if char == ".":
                continue

            color = colors.get(char, BLACK)

            px = ox + (x - len(row) // 2) * pixel
            py = oy + (y - len(sprite) // 2) * pixel - 6

            pygame.draw.rect(
                screen,
                color,
                (px, py, pixel, pixel)
            )

    angle = -pygame.Vector2(1, 0).angle_to(direction)
    rotated_ak = pygame.transform.rotate(ak_img, angle)
    weapon_pos = center + direction * 30

    weapon_rect = rotated_ak.get_rect(
        center=(int(weapon_pos.x), int(weapon_pos.y))
    )

    screen.blit(rotated_ak, weapon_rect)