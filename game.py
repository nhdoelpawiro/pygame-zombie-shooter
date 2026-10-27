import pygame
import random
import math
from map import make_forest, draw_forest

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dead Woods")
clock = pygame.time.Clock()

# -------------------- IMAGES --------------------

def remove_background(image):
    image = image.convert_alpha()

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, a = image.get_at((x, y))

            # Remove black and white backgrounds
            if r < 30 and g < 30 and b < 30:
                image.set_at((x, y), (r, g, b, 0))
            elif r > 235 and g > 235 and b > 235:
                image.set_at((x, y), (r, g, b, 0))

    return image


# AK-47
ak_img = pygame.image.load(
    "./ak47.png"
).convert_alpha()

ak_img = pygame.transform.scale(ak_img, (90, 60))

# Normal zombie
zombie_image = pygame.image.load(
    "zombie_image.jpeg"
).convert()

zombie_image = pygame.transform.scale(
    zombie_image, (75, 95)
)
zombie_image = remove_background(zombie_image)

# Fast zombie
snelle_image = pygame.image.load(
    "snelle_image.png"
).convert()

snelle_image = pygame.transform.scale(
    snelle_image, (60, 75)
)
snelle_image = remove_background(snelle_image)

# Tank zombie
tank_image = pygame.image.load(
    "tank_image.webp"
).convert()

tank_image = pygame.transform.scale(
    tank_image, (90, 105)
)
tank_image = remove_background(tank_image)

# Boss zombie
boss_image = pygame.image.load(
    "boss_image.png"
).convert()

boss_image = pygame.transform.scale(
    boss_image, (100, 120)
)
boss_image = remove_background(boss_image)


# -------------------- AUDIO --------------------

if not pygame.mixer.get_init():
    pygame.mixer.init()

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


# -------------------- COLORS --------------------

WHITE = (235, 235, 225)
RED = (190, 45, 45)
BLACK = (20, 20, 20)
YELLOW = (235, 205, 70)


# -------------------- FONTS --------------------

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 90)
small_font = pygame.font.Font(None, 24)


# -------------------- GAME VARIABLES --------------------

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


# -------------------- CREATE ZOMBIES --------------------

def new_zombie(zombie_type="normal"):
    side = random.choice(
        ["top", "bottom", "left", "right"]
    )

    offsets = {
        "top": (random.randint(-700, 700), -600),
        "bottom": (random.randint(-700, 700), 600),
        "left": (-600, random.randint(-400, 400)),
        "right": (600, random.randint(-400, 400))
    }

    x, y = offsets[side]
    pos = player + pygame.Vector2(x, y)

    if zombie_type == "normal":
        return {
            "pos": pos,
            "speed": random.uniform(0.7, 1.2),
            "max_hp": 2,
            "hp": 2,
            "type": "normal",
            "size": 15
        }

    elif zombie_type == "fast":
        return {
            "pos": pos,
            "speed": random.uniform(2.0, 2.8),
            "max_hp": 1,
            "hp": 1,
            "type": "fast",
            "size": 12
        }

    elif zombie_type == "tank":
        return {
            "pos": pos,
            "speed": random.uniform(0.4, 0.7),
            "max_hp": 12,
            "hp": 12,
            "type": "tank",
            "size": 20
        }

    elif zombie_type == "boss":
        return {
            "pos": pos,
            "speed": 0.5,
            "max_hp": 20,
            "hp": 20,
            "type": "boss",
            "size": 30
        }


# -------------------- ZOMBIE SOUNDS --------------------

def play_zombie_sound():
    for channel in zombie_channels:
        if not channel.get_busy():
            channel.play(random.choice(zombie_sounds))
            return


# -------------------- START A ROUND --------------------

def start_round():
    global round_timer, zombie_sound_timer

    zombies.clear()
    bullets.clear()

    amount = 10 + (round_no - 1) * 15

    for _ in range(amount):
        chance = random.random()

        # Rounds 1-2: normal zombies
        if round_no <= 2:
            zombie_type = "normal"

        # Rounds 3-4: introduce fast zombies
        elif round_no <= 4:
            if chance < 0.20:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        # Rounds 5-6: introduce tank zombies
        elif round_no <= 6:
            if chance < 0.15:
                zombie_type = "tank"
            elif chance < 0.35:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        # Rounds 7-8: stronger zombie combinations
        elif round_no <= 8:
            if chance < 0.10:
                zombie_type = "tank"
            elif chance < 0.35:
                zombie_type = "fast"
            else:
                zombie_type = "normal"

        # Rounds 9-10: introduce bosses
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

    round_timer = 90
    zombie_sound_timer = 120


# -------------------- UPDATE ZOMBIES --------------------

def update_zombies():
    global health, zombie_sound_timer

    for zombie in zombies:
        direction = player - zombie["pos"]

        if direction.length_squared() > 0:
            direction = direction.normalize()
            zombie["pos"] += direction * zombie["speed"]

        hit_distance = 18 + zombie["size"]

        if zombie["pos"].distance_to(player) < hit_distance:
            health = max(0, health - 1)

            if direction.length_squared() > 0:
                zombie["pos"] -= direction * 8

            play_zombie_sound()

    if zombies:
        zombie_sound_timer -= 1

        if zombie_sound_timer <= 0:
            play_zombie_sound()
            zombie_sound_timer = random.randint(120, 300)


# -------------------- DRAW ZOMBIES --------------------

def draw_zombies():
    time = pygame.time.get_ticks()

    for z in zombies:
        # Convert world coordinates to screen coordinates
        p = z["pos"] - camera + pygame.Vector2(
            WIDTH // 2, HEIGHT // 2
        )

        # Skip zombies far outside the screen
        if not screen.get_rect().inflate(
            200, 200
        ).collidepoint(p):
            continue

        # Select the correct image
        if z["type"] == "normal":
            image = zombie_image
        elif z["type"] == "fast":
            image = snelle_image
        elif z["type"] == "tank":
            image = tank_image
        else:
            image = boss_image

        # Walking animation
        bob = math.sin(
            time * 0.012 * (z["speed"] + 1)
        ) * 4

        # Slight tilting animation
        angle = math.sin(
            time * 0.008 * (z["speed"] + 1)
        ) * 8

        rotated_image = pygame.transform.rotate(
            image, angle
        )

        rect = rotated_image.get_rect(
            center=(int(p.x), int(p.y + bob))
        )

        screen.blit(rotated_image, rect)

        # Zombie health bar
        size = z["size"]
        bar_width = size * 2

        hp_ratio = max(
            0, z["hp"] / z["max_hp"]
        )

        bar_x = int(p.x - size)
        bar_y = int(p.y - size - 8)

        pygame.draw.rect(
            screen,
            RED,
            (bar_x, bar_y, bar_width, 5)
        )

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (
                bar_x,
                bar_y,
                int(bar_width * hp_ratio),
                5
            )
        )


# -------------------- UPDATE PLAYER --------------------

def update_player():
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

    camera.update(player)




# -------------------- DRAW PLAYER --------------------

def draw_player():
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)

    mouse = pygame.Vector2(pygame.mouse.get_pos())
    direction = mouse - center

    if direction.length_squared() > 0:
        direction = direction.normalize()
    else:
        direction = pygame.Vector2(1, 0)

    pixel = 2
    ox, oy = int(center.x), int(center.y)

    # Player colors
    BLACK = (10, 10, 12)
    HAIR = (25, 20, 35)
    SKIN = (230, 175, 145)
    SCARF = (130, 50, 110)
    SHIRT = (25, 25, 30)
    PANTS = (190, 190, 195)
    BELT = (20, 20, 25)

    # Pixel-art player sprite
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

    # Draw player body
    for y, row in enumerate(sprite):
        for x, char in enumerate(row):
            if char == ".":
                continue

            color = {
                "H": HAIR,
                "S": SKIN,
                "s": SKIN,
                "P": SCARF,
                "C": SHIRT,
                "c": SHIRT,
                "W": PANTS,
                "w": PANTS,
                "B": BELT,
            }.get(char, BLACK)

            px = ox + (x - len(row) // 2) * pixel
            py = oy + (y - len(sprite) // 2) * pixel - 6

            pygame.draw.rect(
                screen,
                color,
                (px, py, pixel, pixel)
            )

    # Rotate the AK-47 toward the mouse
    angle = -pygame.Vector2(1, 0).angle_to(direction)

    rotated_ak = pygame.transform.rotate(ak_img, angle)

    # Position the AK in front of the player
    weapon_pos = center + direction * 25

    weapon_rect = rotated_ak.get_rect(
        center=(int(weapon_pos.x), int(weapon_pos.y))
    )

    screen.blit(rotated_ak, weapon_rect)



# -------------------- SHOOTING --------------------

def shoot():
    center = pygame.Vector2(
        WIDTH // 2, HEIGHT // 2
    )

    direction = (
        pygame.Vector2(pygame.mouse.get_pos()) - center
    )

    if direction.length_squared() == 0:
        return

    direction = direction.normalize()

    bullets.append({
        "pos": player + direction * 35,
        "vel": direction * 12
    })

    shoot_channel.play(shoot_sound)


# -------------------- UPDATE BULLETS --------------------

def update_bullets():
    for bullet in bullets[:]:
        bullet["pos"] += bullet["vel"]

        if bullet["pos"].distance_to(player) > 1200:
            bullets.remove(bullet)
            continue

        for zombie in zombies[:]:
            hit_radius = zombie["size"] + 5

            if bullet["pos"].distance_to(
                zombie["pos"]
            ) < hit_radius:

                bullets.remove(bullet)
                zombie["hp"] -= 1

                if zombie["hp"] <= 0:
                    zombies.remove(zombie)

                break


# -------------------- DRAW BULLETS --------------------

def draw_bullets():
    for bullet in bullets:
        pos = bullet["pos"] - camera + pygame.Vector2(
            WIDTH // 2, HEIGHT // 2
        )

        if screen.get_rect().collidepoint(pos):
            pygame.draw.circle(
                screen,
                YELLOW,
                (int(pos.x), int(pos.y)),
                4
            )
# -------------------- DRAW TEXT --------------------

def draw_text(text, text_font, color, position):
    image = text_font.render(text, True, color)
    screen.blit(image, image.get_rect(center=position))


# -------------------- GAME UI --------------------

def draw_game_ui():
    pygame.draw.rect(screen, BLACK, (15, 15, 205, 35))

    pygame.draw.rect(
        screen, RED,
        (18, 18, max(0, health) * 2, 29)
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
        small_font.render(
            f"Zombies: {len(zombies)}", True, WHITE
        ),
        (WIDTH - 190, 52)
    )


# -------------------- BUTTONS --------------------

def make_button(text, y, height=70):
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


# -------------------- MAIN MENU --------------------

def menu():
    screen.fill(BLACK)

    draw_text(
        "DEAD WOODS",
        big_font,
        WHITE,
        (WIDTH // 2, 190)
    )

    draw_text(
        "Survive 10 rounds in the forest",
        font,
        (175, 180, 165),
        (WIDTH // 2, 255)
    )

    button = make_button("START GAME", 330, 75)

    draw_text(
        "WASD = Move   Mouse = Aim   Left Click = Shoot",
        small_font,
        WHITE,
        (WIDTH // 2, 470)
    )

    return button


# -------------------- GAME OVER SCREEN --------------------

def end_screen():
    screen.fill(BLACK)

    title = "YOU DIED" if health <= 0 else "YOU SURVIVED!"
    color = RED if health <= 0 else WHITE

    draw_text(
        title,
        big_font,
        color,
        (WIDTH // 2, 220)
    )

    return make_button("PLAY AGAIN", 320)


# -------------------- RESET GAME --------------------

def reset_game():
    global health, round_no, game_over
    global shoot_timer, zombie_sound_timer

    health = 100
    round_no = 1
    game_over = False
    shoot_timer = 0
    zombie_sound_timer = 120

    player.update(0, 160)
    camera.update(player)

    bullets.clear()
    zombies.clear()
    trees.clear()

    trees.extend(make_forest())

    # Stop zombie sounds
    for channel in zombie_channels:
        channel.stop()

    walk_channel.stop()
    shoot_channel.stop()

    # Restart music
    menu_music.stop()
    music.stop()
    music.play(-1)

    start_round()


# -------------------- INITIALIZE FOREST --------------------

trees.extend(make_forest())

start_button = None
restart_button = None

running = True


# -------------------- MAIN GAME LOOP --------------------

while running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            # Start game
            if not game_started and start_button:
                if start_button.collidepoint(event.pos):
                    game_started = True
                    reset_game()

            # Restart game
            elif game_over and restart_button:
                if restart_button.collidepoint(event.pos):
                    reset_game()

            # Shoot
            elif game_started and not game_over:
                if shoot_timer <= 0:
                    shoot()
                    shoot_timer = 10

    # Main menu
    if not game_started:
        start_button = menu()
        pygame.display.flip()
        continue

    # Game over screen
    if game_over:
        restart_button = end_screen()
        pygame.display.flip()
        continue

    # Update game
    update_player()
    update_bullets()
    update_zombies()

    shoot_timer = max(0, shoot_timer - 1)
    round_timer = max(0, round_timer - 1)

    # Check health
    if health <= 0:
        game_over = True

    # Check round progression
    elif not zombies and round_timer == 0:
        if round_no < 10:
            round_no += 1
            start_round()
        else:
            game_over = True

    # Stop sounds on game over
    if game_over:
        music.stop()
        walk_channel.stop()

        for channel in zombie_channels:
            channel.stop()

    # Draw forest using the original camera
    draw_forest(screen, trees, camera)

    # Draw game objects
    draw_zombies()
    draw_bullets()
    draw_player()
    draw_game_ui()

    if round_timer > 0:
        draw_text(
            f"ROUND {round_no}",
            big_font,
            RED,
            (WIDTH // 2, HEIGHT // 2)
        )

    pygame.display.flip()

pygame.quit()