import config
import pygame
import copy
from random import seed
from timeit import default_timer as time
from meta import *
from util_objects import *
from game_objects import *
from enemies import *


log = create_logger("main")


class Game:
    def __init__(self):
        """This is the creation of a Game object (the window and things required for the window).
        Things that are required to start a game but not to run the window should go in setup()."""
        self.screen = pygame.display.set_mode(config.window.size)
        self.current_screen = Screen.Welcome
        self.running = True
        self.drawables = []
        self.simulatables = []
        self.default_font = None  # used by FontDrawable objects as the default font.
        self.enemies_last_bounce_side = None
        self.play_status = False  # Sets the playable status of the game
        self.game_over = False  #  is set to True when the player loses the game. This will allow the Game over screen to come up.
        self.donePlay = False

        self.finishSound = pygame.mixer.Sound("resources/sounds/finish.wav")

    def __collidable_object_filter__(self, obj):
        if obj.valid_screens is not None:
            if isinstance(obj.valid_screens, Screen):
                if self.current_screen != obj.valid_screens: return False
            elif isinstance(obj.valid_screens, tuple):
                if self.current_screen not in obj.valid_screens: return False
        return True


    def change_screen(self, new_screen):
        if not isinstance(new_screen, Screen):
            raise TypeError('Need to use the Screen objects above like `Screen.Welcome`.')

        self.current_screen = new_screen

        match new_screen:
            case Screen.Welcome:
                self.reload_screen_welcome(self.current_screen)
            case Screen.GameOver:
                self.reload_screen_gameover(self.current_screen)
            case Screen.Level1:
                self.reload_screen_level1(self.current_screen)
            case Screen.Level2:
                self.reload_screen_level2(self.current_screen)
            case Screen.Level3:
                self.reload_screen_level3(self.current_screen)


    def collidable_objects(self):
        return filter(self.__collidable_object_filter__, self.simulatables)


    def visible_enemies(self):
        return list(filter(self.__collidable_object_filter__, self.enemies))


    def exit(self):
        self.running = False


    def run(self):
        """This is called to start running the game."""
        self.clock = Clock()
        seed(time())
        self.setup()
        while self.running:
            self.loop()
            self.clock.tick(config.window.fps_limit)


    def setup(self):
        """Called once when the game first starts."""
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)

        pygame.mixer.pre_init(44100, -16, 2, 512)
        config.music.loadMusic(self, 1)

        pygame.display.set_caption(config.window.title)

        self.default_font = pygame.font.Font(config.window.font, 24)

        self.btn_font = pygame.font.Font(None, 30)

        self.backgroundmain = Background(img=config.assets.background.main, game=self, valid_screens=Screen.Welcome)
        self.background1 = Background(img=config.assets.background.level1, game=self, valid_screens=Screen.Level1)
        self.background2 = Background(img=config.assets.background.level2, game=self, valid_screens=Screen.Level2)
        self.background3 = Background(img=config.assets.background.level3, game=self, valid_screens=Screen.Level3)
        self.backgroundgame = Background(img=config.assets.background.main, game=self, valid_screens=Screen.GameOver)

        self.score = Text(
            colour=(config.window.score_colour),
            game=self,
            position=(10, 10),
            value=0
        )

        self.CHECKLEVEL = pygame.event.custom_type()


        self.player = Player(game=self, img=config.game.player_image1,
                             valid_screens=(Screen.Level1, Screen.Level2, Screen.Level3),
                             position = Coord(config.window.size[0] / 2 - config.game.player_size.x / 2, 600), sound=config.music.bullet1)

        self.RELOAD = pygame.event.custom_type()

        # Create some example enemies
        self.enemies = []
        self.bullets = []

        self.welcomeScreen = WelcomeScreen(game=game, valid_screens=Screen.Welcome)
        self.gameOverScreen = GameOverScreen(game=game, valid_screens=Screen.GameOver)

        self.change_screen(Screen.Welcome)


    def loop(self):
        """Run every frame."""
        self.handle_events()
        self.simulate()
        self.draw()


    def simulate(self):
        """Performs moving of objects, collisions, any simulation tasks."""
        for simulatable in self.simulatables:
            simulatable.__isimulate__()


    def draw(self):
        """Clears and redraws the screen."""
        self.screen.fill((0, 0, 0))

        for drawable in self.drawables:
            drawable.__draw__(self.screen)

        log.debug(f'FPS is {self.clock.get_fps()}')

        pygame.display.update()


    def handle_events(self):
        """Handle user input events here. Could also be used for custom events if we want."""
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False

                case pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.velocity.x -= 3

                    elif event.key == pygame.K_RIGHT:
                        self.player.velocity.x += 3

                    elif event.key == pygame.K_SPACE:
                        self.player.fire_bullet()

                case pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.velocity.x += 3

                    elif event.key == pygame.K_RIGHT:
                        self.player.velocity.x -= 3

                case self.RELOAD:
                    self.player.loaded = True
                    pygame.time.set_timer(self.RELOAD, 0)

                case self.CHECKLEVEL:
                    numEnemies = len(self.visible_enemies())
                    #print(numEnemies)
                    self.attempt_update_level(numEnemies)


    def attempt_update_level(self, ind):
        if ind == 0:
            match self.current_screen:
                case Screen.Level1:
                    self.change_screen(Screen.Level2)
                    self.score.update(f"{int(self.score.get_content()) + 420}")
                case Screen.Level2:
                    self.change_screen(Screen.Level3)
                    self.score.update(f"{int(self.score.get_content()) + 420}")
                case Screen.Level3:
                    if not self.donePlay:
                        self.donePlay = True
                        self.score.update(f"{int(self.score.get_content()) + 2321}")
                        pygame.time.set_timer(self.RELOAD, 0)


    def generate_enemies(self, size, enemy_class, class_num, second_size=None, second_class=None, class_num_two=None):
        for y in range(size[1]):
            for x in range(size[0]):
                enemy_class(
                    game=self,
                    position=Coord(x * config.game.grid_size.x + 100, y * config.game.grid_size.y + 20),
                    valid_screens=copy.copy(self.current_screen),
                    name=f"({x}, {y})",
                    points=config.game.enemy_points[class_num]
                )

        if second_class is None:
            return

        for y in range(second_size[1]):
            for x in range(second_size[0]):
                second_class(
                    game=self,
                    position=Coord(x * config.game.grid_size.x + 100, y * config.game.grid_size.y + 50),
                    valid_screens=copy.copy(self.current_screen),
                    name=f"({x}, {y})",
                    points=config.game.enemy_points[class_num_two]
                )


    def clear_enemies(self):
        enemies_copy = copy.copy(self.enemies)
        for e in enemies_copy:
            e.delete()
        del enemies_copy

        bullets_copy = copy.copy(self.bullets)
        for b in self.bullets:
            b.delete()
        del bullets_copy

        for d in self.simulatables:
            if isinstance(d, Enemy):
                log.warning(f'Enemy {d} still exists in simulatables after a clear?')
                self.simulatables.remove(d)
            elif isinstance(d, Bullet):
                log.warning(f'Bullet {d} still exists in simulatables after a clear?')
                self.simulatables.remove(d)

        for d in self.drawables:
            if isinstance(d, Enemy):
                log.warning(f'Enemy {d} still exists in drawables after a clear?')
                self.drawables.remove(d)
            if isinstance(d, Bullet):
                log.warning(f'Bullet {d} still exists in drawables after a clear?')
                self.drawables.remove(d)


    def reload_screen_welcome(self, old_screen):
        log.debug('Switched to welcome screen')
        self.clear_enemies()
        config.music.loadMusic(self, Screen.Welcome)


    def reload_screen_gameover(self, old_screen):
        log.debug('Switched to game-over screen')
        self.clear_enemies()
        config.music.loadMusic(self, Screen.GameOver)
        pygame.mixer.Sound.play(self.finishSound)
        pygame.time.set_timer(self.CHECKLEVEL, 0)
        self.clear_enemies

    def reload_screen_level1(self, old_screen):
        log.debug('Switched to level 1')
        self.clear_enemies()
        self.generate_enemies(config.game.level1.num_enemies, Frigate, 0)
        self.player.reload_timer = config.game.player_reload[0]
        config.music.loadMusic(self, Screen.Level1)
        self.player.sound =config.music.bullet1
        self.score.update(f"0")
        pygame.time.set_timer(self.CHECKLEVEL, 950)


    def reload_screen_level2(self, old_screen):
        log.debug('Switched to level 2')
        self.player.img = config.game.player_image2
        self.player.size = config.game.player_size
        self.clear_enemies()
        self.generate_enemies(config.game.level2.num_enemies, Frigate, 0, config.game.level2.strong_enemies, Carrier, 1)
        self.player.reload_timer = config.game.player_reload[1]
        config.music.loadMusic(self, Screen.Level2)
        self.player.sound=config.music.bullet2
        pygame.mixer.Sound.play(self.finishSound)



    def reload_screen_level3(self, old_screen):
        log.debug('Switched to level 3')
        self.player.img = config.game.player_image3
        self.player.size = config.game.player_size
        self.clear_enemies()
        self.generate_enemies(config.game.level3.num_enemies, Carrier, 1, config.game.level3.strong_enemies, Buff, 2)
        self.player.reload_timer = config.game.player_reload[2]
        config.music.loadMusic(self, Screen.Level3)
        self.player.sound = config.music.bullet3
        pygame.mixer.Sound.play(self.finishSound)

if __name__ == "__main__":
    game = Game()
    game.run()
