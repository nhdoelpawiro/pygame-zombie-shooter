import math
import random
import pygame

from settings import WIDTH, HEIGHT, RED

def load_zombie_images():
    def load_image(path, size):
        image = pygame.image.load(path).convert()
        image = pygame.transform.scale(image, size)
        return remove_background(image)

    return {
        "normal": load_image("assets/zombie_image.jpeg", (75, 95)),
        "fast": load_image("assets/snelle_image.png", (60, 75)),
        "tank": load_image("assets/tank_image.webp", (90, 105)),
        "boss": load_image("assets/boss_image.png", (100, 120)),
    }


def remove_background(image):
    image = image.convert_alpha()

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, a = image.get_at((x, y))

            if r < 30 and g < 30 and b < 30:
                image.set_at((x, y), (r, g, b, 0))
            elif r > 235 and g > 235 and b > 235:
                image.set_at((x, y), (r, g, b, 0))

    return image


def new_zombie(zombie_type="normal"):
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        pos = (random.randint(0, WIDTH), -30)
    elif side == "bottom":
        pos = (random.randint(0, WIDTH), HEIGHT + 30)
    elif side == "left":
        pos = (-30, random.randint(70, HEIGHT))
    else:
        pos = (WIDTH + 30, random.randint(70, HEIGHT))

    stats = {
        "normal": (0.7, 1.2, 2, 15),
        "fast": (2.0, 2.8, 1, 12),
        "tank": (0.4, 0.7, 12, 20),
        "boss": (0.5, 0.5, 20, 30),
    }

    min_speed, max_speed, hp, size = stats[zombie_type]

    return {
        "pos": pygame.Vector2(pos),
        "speed": random.uniform(min_speed, max_speed),
        "max_hp": hp,
        "hp": hp,
        "type": zombie_type,
        "size": size,
    }


def start_round(zombies, round_no):
    amount = 10 + (round_no - 1) * 5

    for _ in range(amount):
        chance = random.random()

        if round_no <= 2:
            kind = "normal"
        elif round_no <= 4:
            kind = "fast" if chance < 0.20 else "normal"
        elif round_no <= 6:
            kind = (
                "tank" if chance < 0.15
                else "fast" if chance < 0.35
                else "normal"
            )
        elif round_no <= 8:
            kind = (
                "tank" if chance < 0.10
                else "fast" if chance < 0.35
                else "normal"
            )
        else:
            kind = (
                "boss" if chance < 0.10
                else "tank" if chance < 0.25
                else "fast" if chance < 0.50
                else "normal"
            )

        zombies.append(new_zombie(kind))


def update_zombies(zombies, player, health):
    """Move zombies toward the player and return updated health."""
    for zombie in zombies:
        direction = player - zombie["pos"]

        if direction.length_squared() == 0:
            continue

        direction = direction.normalize()
        zombie["pos"] += direction * zombie["speed"]

        # Damage the player when a zombie gets close.
        if zombie["pos"].distance_to(player) < zombie["size"] + 12:
            health -= 0.2

    return max(0, health)


def draw_zombies(screen, zombies, images, camera):
    time = pygame.time.get_ticks()
    screen_center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    for zombie in zombies:
        p = zombie["pos"]
        size = zombie["size"]

        image = images[zombie["type"]]
        bob = math.sin(time * 0.012 * (zombie["speed"] + 1)) * 4
        angle = math.sin(time * 0.008 * (zombie["speed"] + 1)) * 8

        rotated = pygame.transform.rotate(image, angle)

        screen_pos = p - camera + screen_center
        rect = rotated.get_rect(
            center=(int(screen_pos.x), int(screen_pos.y + bob))
        )
        screen.blit(rotated, rect)

        ratio = max(0, zombie["hp"] / zombie["max_hp"])
        bar_x = int(screen_pos.x - size)
        bar_y = int(screen_pos.y - size - 8)

        pygame.draw.rect(screen, RED, (bar_x, bar_y, size * 2, 4))
        pygame.draw.rect(
            screen, (0, 255, 0),
            (bar_x, bar_y, int(size * 2 * ratio), 4)
        )