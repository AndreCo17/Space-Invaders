import pygame
import config
import copy
import random
import traceback
from basic_objects import *
from util_objects import *
from math import copysign
from meta import create_logger
from random import randint


log = create_logger('game_objects')


class GameOverScreen(Drawable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Game Over Title Banner
        self.gmOver = renderImage(
            " ",
            self.game.btn_font,
            config.window.size[0] / 2 - config.assets.bnrGmOver.get_width() / 4,
            config.window.size[1] / 2 - config.assets.bnrGmOver.get_height() / 2,
            config.assets.bnrGmOver,
            config.assets.overlay,
            0.5,
        )
        # Play AGain Button
        self.btnPlayAgn = renderImage(
            "Play Again",
            self.game.btn_font,
            config.window.size[0] / 2 - config.assets.bBlueGrn.get_width() / 5,
            config.window.size[1] / 2 + config.assets.bBlueGrn.get_height() / 8,
            config.assets.bBlueGrn,
            config.assets.bPurple,
            0.4,
        )
        # Exit Button
        self.btnExit = renderImage(
            "Exit",
            self.game.btn_font,
            config.window.size[0] / 2 - config.assets.bBlueGrn.get_width() / 5,
            config.window.size[1] / 2 + config.assets.bBlueGrn.get_height() / 1.5,
            config.assets.bBlueGrn,
            config.assets.bPurple,
            0.4,
        )


    def __draw__(self, screen):
        if not self.visible: return
        if self.valid_screens is not None:
            if isinstance(self.valid_screens, Screen):
                if self.game.current_screen != self.valid_screens: return False
            elif isinstance(self.valid_screens, tuple):
                if self.game.current_screen not in self.valid_screens: return False

        self.gmOver.draw(screen, False)
        if self.btnPlayAgn.draw(screen, True):
            self.game.change_screen(Screen.Level1)
        if self.btnExit.draw(screen, True):
            self.game.exit()


class WelcomeScreen(Drawable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bnrWelcome = renderImage(
            " ",  # button text
            self.game.btn_font,  # text font
            config.window.size[0] / 2
            - config.assets.bnrWelcome.get_width() / 4,  # x pos
            config.window.size[1] / 2
            - config.assets.bnrWelcome.get_height() / 2,  # y pos
            config.assets.bnrWelcome,  # Welcome Banner
            config.assets.overlay,  # overlay
            0.5,  # scale
        )
        # Play Button
        self.btnPlay = renderImage(
            "Play",  # button text
            self.game.btn_font,  # text font
            config.window.size[0] / 2
            - config.assets.bBlueGrn.get_width() / 5,  # x pos
            config.window.size[1] / 2
            + config.assets.bBlueGrn.get_height() / 8,  # y pos
            config.assets.bBlueGrn,  # Default button image
            config.assets.bPurple,  # Clicked button image
            0.4,  # scale
        )
        # Exit Button
        self.btnExit = renderImage(
            "Exit",
            self.game.btn_font,
            config.window.size[0] / 2 - config.assets.bBlueGrn.get_width() / 5,
            config.window.size[1] / 2 + config.assets.bBlueGrn.get_height() / 1.5,
            config.assets.bBlueGrn,
            config.assets.bPurple,
            0.4,
        )

        if 'position' in kwargs: del kwargs['position']
        if 'size' in kwargs: del kwargs['size']
        if 'img' in kwargs: del kwargs['img']


    def __draw__(self, screen):
        if not self.visible: return
        if self.valid_screens is not None:
            if isinstance(self.valid_screens, Screen):
                if self.game.current_screen != self.valid_screens: return False
            elif isinstance(self.valid_screens, tuple):
                if self.game.current_screen not in self.valid_screens: return False

        self.bnrWelcome.draw(screen, False)
        if self.btnPlay.draw(screen, True):
            self.game.play_status = True
            self.game.change_screen(Screen.Level1)
        if self.btnExit.draw(screen, True):
            self.game.exit()


class Text(Drawable):
    """Some text that will be drawn on the screen."""

    def __init__(self, font=None, *, colour, value, **kwargs):
        self.value = value
        self.colour = colour
        self.font = font

        # initialize the Drawable object that this inherits from, also pass any unexpected key=value arguments to the Drawable object.
        super().__init__(**kwargs)

    def update(self, newString):
        self.value = newString

    def get_content(self):
        return self.value

    def __draw__(self, screen):
        if self.font is None:
            surface = self.game.default_font.render(
                f"{self.value}", config.window.text_antialias, self.colour
            )
        else:
            surface = self.font.render(
                f"{self.value}", config.window.text_antialias, self.colour
            )

        screen.blit(surface, (self.x, self.y))


class Background(Drawable):
    """A background image that will be drawn on the screen."""

    def __init__(self, **kwargs):
        if "position" not in kwargs:
            kwargs["position"] = Coord(0, 0)
        if "size" not in kwargs:
            kwargs["size"] = Coord(config.window.size[0], config.window.size[1])

        # initialize the Drawable object that this inherits from, also pass any unexpected key=value arguments to the Drawable object.
        super().__init__(**kwargs)


class Player(Simulatable):
    """The player ship."""

    def __init__(self, **kwargs):
        if "img" not in kwargs:
            kwargs["img"] = pygame.image.load("resources/spaceship.png")

        if "position" not in kwargs:
            kwargs["position"] = Coord(370, 480)

        if "size" not in kwargs:
            kwargs["size"] = copy.copy(config.game.player_size)

        self.loaded = True
        self.reload_timer = config.game.player_reload[0]

        super().__init__(**kwargs)

    
    def collide_callback(self, obj):
        if isinstance(obj, Enemy):
            self.game.change_screen(Screen.GameOver)


    def __bounce_screen_edges__(self):
        if self.position.x <= 0:
            self.position.x = 0
        elif self.position.x + self.size.x >= config.window.size[0] - 1:
            self.position.x = config.window.size[0] - 1 - self.size.x


    def hit_by_bullet(self, bullet):
        if isinstance(bullet.source, Player): return
        self.game.change_screen(Screen.GameOver)
        bullet.delete()


    def fire_bullet(self):
        if self.loaded:
            Bullet(
                position=self.position,
                game=self.game,
                velocity=Velocity(x_y=(0, config.game.bullet_speed)),
                source=self
            )
            pygame.mixer.Sound.play(self.sound)
            self.loaded = False
            pygame.time.set_timer(self.game.RELOAD, self.reload_timer)


    def changeImage(self, level):
        if(level==1):
            self.img = config.game.player_image1
        elif(level==2):
            self.img = config.game.player_image2
        elif(level==3):
            self.img = config.game.player_image3


class Bullet(Simulatable):
    def __init__(self, *, source, **kwargs):
        if "img" not in kwargs:
            kwargs["img"] = config.game.bullet_img

        if "position" not in kwargs:
            kwargs["position"] = Coord(370, 480)

        if "size" not in kwargs:
            kwargs["size"] = copy.copy(config.game.player_size)

        if "bounce_screen_edges" not in kwargs:
            kwargs["bounce_screen_edges"] = False

        if "collide" not in kwargs:
            kwargs["collide"] = False

        self.source = source

        super().__init__(**kwargs)

        self.game.bullets.append(self)


    def delete(self):
        if self in self.game.bullets:
            self.game.bullets.remove(self)
        super().delete()


    def __isimulate__(self):
        if isinstance(self.source, Player):
            log.debug(f'Bullet position: {self.x, self.y}')
        if super().__isimulate__():
            if self.position.y <= 0:
                self.delete()
            elif self.position.y >= config.window.size[1] - 1:
                self.delete()


    def __eq__(self, other):
        return self is other


    def collide_callback(self, obj):
        if isinstance(obj, Simulatable):
            obj.hit_by_bullet(self)


class Enemy(Simulatable):
    """A single enemy ship."""

    def __init__(self, points, *, bullet_speed, fire_chance, **kwargs):

        self.points = points
        self.bullet_speed = bullet_speed
        self.fire_chance = fire_chance

        super().__init__(**kwargs)

        self.game.enemies.append(self)


    def __eq__(self, other):
        return self is other


    def __str__(self):
        if self.name is not None:
            return f"{__class__.__name__}-{self.name}"
        else:
            return super().__str__()


    def delete(self):
        """Delete all references to this enemy so they are removed from memory."""
        if self in self.game.enemies:
            self.game.enemies.remove(self)
        super().delete()


    def hit_by_bullet(self, bullet):
        if isinstance(bullet.source, Enemy): return
        log.debug("Enemy was hit by a bullet!")
        self.delete()
        bullet.delete()
        self.game.score.update(f"{int(self.game.score.get_content()) + self.points}")


    def screen_edge_callback(self, side):
        super().screen_edge_callback(side)

        if self.game.enemies_last_bounce_side != side:
            log.debug(f'Hit new screen edge {self.game.enemies_last_bounce_side} to {side}')
            for enemy in self.game.visible_enemies():
                enemy.position.y += config.game.enemy_down_shift
                enemy.y += config.game.enemy_down_shift
            self.game.enemies_last_bounce_side = side


    def __isimulate__(self):
        if super().__isimulate__():
            if self.y >= 700:
                self.game.change_screen(Screen.GameOver)
            if random.random() < self.fire_chance:
                self.fire_bullet()


    def fire_bullet(self):
        bullet_img = config.game.bullet_enemy_img[2]
        if self.points == 75:
            bullet_img = config.game.bullet_enemy_img[1]
        elif self.points == 50:
            bullet_img = config.game.bullet_enemy_img[0]
        Bullet(
            position=self.position,
            game=self.game,
            velocity=Velocity(x_y=(0, self.bullet_speed)),
            source=self,
            img=bullet_img
        )


class renderImage:
    def __init__(self, btn_text, gui, x, y, btn, btnClicked, scale):
        self.btn_text = btn_text
        self.gui = gui
        self.x = x
        self.y = y
        self.btn = btn
        self.scale = scale
        self.width = self.btn.get_width()
        self.height = self.btn.get_height()
        self.image = pygame.transform.scale(
            self.btn,
            (int(self.width * self.scale), int(self.height * self.scale)),
        )
        self.btnClicked = pygame.transform.scale(
            btnClicked,
            (int(self.width * self.scale), int(self.height * self.scale)),
        )
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.topleft = (x, y)
        self.text = self.gui.render(self.btn_text, True, "white")
        self.text_rect = self.text.get_rect(
            center=(
                self.x + self.image.get_width() / 2,
                self.y + self.image.get_height() / 2,
            )
        )
        self.clicked = False

    # Draw the image on the screen,
    def draw(self, screen, clickable):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        if clickable:
            # check mouse over and click condition
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.image = self.btnClicked
                    self.clicked = True

                # when mouse button is released
                if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                    self.image = pygame.transform.scale(
                        self.btn,
                        (int(self.width * self.scale), int(self.height * self.scale)),
                    )
                    self.clicked = False
                    action = True

        # draw button on screen
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

        return action
