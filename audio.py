import pygame

def load_audio():
    music = pygame.mixer.Sound("./sfx/banditradio.mp3")
    menu_music = pygame.mixer.Sound("./sfx/menu.mp3")
    shoot_sound = pygame.mixer.Sound("./sfx/shoot.mp3")
    walk_sound = pygame.mixer.Sound("./sfx/walk.mp3")

    zombie_sounds = [
        pygame.mixer.Sound(f"./sfx/zombie{i}.mp3")
        for i in range(1, 9)
    ]

    music.set_volume(0.5)
    menu_music.set_volume(0.4)
    shoot_sound.set_volume(0.7)
    walk_sound.set_volume(0.7)

    for sound in zombie_sounds:
        sound.set_volume(0.8)

    return {
        "music": music,
        "menu_music": menu_music,
        "shoot": shoot_sound,
        "walk": walk_sound,
        "zombies": zombie_sounds,
        "walk_channel": pygame.mixer.Channel(1),
        "shoot_channel": pygame.mixer.Channel(2),
        "zombie_channels": [
            pygame.mixer.Channel(i) for i in range(3, 7)
        ],
    }