import pygame
from util_objects import *


class window:
    size = (1024, 720)
    title = 'Space Invaders'
    fps_limit = 50
    fps_history = 10

    font = 'resources/FreeSans.ttf'
    text_antialias = False
    score_colour = (0, 255, 0)


class game:
    player_size = Coord(40, 40)
    player_reload = [800, 600, 300]
    player_image1 = pygame.image.load('resources/spaceship1.png')
    player_image2 = pygame.image.load('resources/spaceship2.png')
    player_image3 = pygame.image.load('resources/spaceship3.png')

    enemy_down_shift = 10

    grid_size = Coord(100, 70)

    bullet_img = pygame.image.load('resources/bullet1.png')
    bullet_enemy_img = [
        pygame.image.load('resources/bulletenemy.png'),
        pygame.image.load('resources/bulletenemy2.png'),
        pygame.image.load('resources/bulletenemy3.png')
        ]
    bullet_speed = -10

    default_rect_colour = (255, 255, 255)

    class level1:
        num_enemies = (5, 4)
    class level2:
        num_enemies = (6, 2)
        strong_enemies = (4, 2)
    class level3:
        num_enemies = (6, 6)
        strong_enemies = (4, 2)

    enemy_points = [50, 75, 120]


class enemy:
    class frigate:
        img = pygame.image.load('resources/enemies/enemy_frigate.png')
        speed = Velocity(x_y=(4, 0))
        size = Coord(40, 40)
        points = 50
        fire_chance = 0.0005
        bullet_speed = 5

    class one:
        img = pygame.image.load('resources/enemies/enemy1.png')
        speed = Velocity(x_y=(6, 0.35))
        size = Coord(40, 40)
        points = 75
        fire_chance = 0.003
        bullet_speed = 6

    class spaceship:
        img = pygame.image.load('resources/enemies/enemy2.png')
        speed = Velocity(x_y=(2, 0.25))
        size = Coord(40, 40)
        points = 120
        fire_chance = 0.00075
        bullet_speed = 7


class logging:
    name_justify_length = 10
    terminal_log_level = 'DEBUG'
    terminal_format = '%(name)s (%(levelname)s): %(message)s'
    logger_specific_levels = {
        'main': 'ERROR',
        'basic_objects': 'INFO',
        'game_objects': 'INFO',
        'game_objects.enemies': 'INFO'
    }


class assets:
    overlay = pygame.image.load('resources/assets/overlay.png')
    # buttons
    bBlueGrn = pygame.image.load('resources/assets/2920872/bBlueGrn.png')
    bPurple = pygame.image.load('resources/assets/2920872/bPurple.png')
    bViolet = pygame.image.load('resources/assets/2920872/bViolet.png')
    # welcome banner
    bnrWelcome = pygame.image.load('resources/assets/bnrWelcome.png')
    # gameover banner
    bnrGmOver = pygame.image.load('resources/assets/bnrGameOver.png')

    class background:
        main = pygame.image.load("./resources/backgrounds/mainbackground.png")
        level1 = pygame.image.load("./resources/backgrounds/background1.png")
        level2 = pygame.image.load("./resources/backgrounds/background2.png")
        level3 = pygame.image.load("./resources/backgrounds/background3.png")

class music:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    bullet1 = pygame.mixer.Sound("./resources/sounds/Level1.mp3")
    bullet2 = pygame.mixer.Sound("./resources/sounds/Level2.mp3")
    bullet3 = pygame.mixer.Sound("./resources/sounds/Level3.mp3")

    def loadMusic(self, level):
        match level:
            case Screen.Welcome:
                pygame.mixer.music.load('resources/background_tracks/main.wav')
                pygame.mixer.music.play(-1)
            case Screen.Level1:
                track2 = pygame.mixer.music.load('resources/background_tracks/lvl1.wav')
                pygame.mixer.music.play(-1)
            case Screen.Level2:
                pygame.mixer.music.load('resources/background_tracks/lvl2.wav')
                pygame.mixer.music.play(-1)
            case Screen.Level3:
                pygame.mixer.music.load('resources/background_tracks/lvl3.wav')
                pygame.mixer.music.play(-1)
            case Screen.GameOver:
                track5= pygame.mixer.music.load('resources/background_tracks/gameover.wav')
                pygame.mixer.music.play(-1)
