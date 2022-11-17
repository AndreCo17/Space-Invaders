import pygame
import config
from util_objects import *
from meta import create_logger


log = create_logger('basic_objects')


class Clock:
    def __init__(self):
        self.start = time()
        self.previous_ticks = DroppingStack(config.window.fps_history)
        self.previous_ticks.put(self.start)
        self.ticks_since_start = 0


    def time(self):
        return time()


    def tick(self, framerate=None):
        cur_tick = time()
        if framerate is not None:
            delay = cur_tick - self.previous_ticks.arr[-1]
            delay = (1 / framerate) - delay
            if delay > 0.0:
                log.debug(f"Delaying frame by {round(delay,4)} seconds")
                sleep(delay)
        self.previous_ticks.put(time())
        self.ticks_since_start += 1


    def avg_frame_time(self):
        avg_time = 0
        if len(self.previous_ticks.arr) == 0:
            return avg_time

        for i in range(len(self.previous_ticks.arr)-1, 0, -1):
            avg_time += self.previous_ticks.arr[i] - self.previous_ticks.arr[i-1]

        if len(self.previous_ticks.arr) > 1:
            avg_time /= len(self.previous_ticks.arr)-1

        return avg_time


    def get_fps(self):
        avg_frame_time = self.avg_frame_time()
        if avg_frame_time == 0:
            return -1
        else:
            return 1 / avg_frame_time


class Drawable(Rect):
    def __init__(self, *, game,
                 img=None,
                 position=Coord(0,0),
                 size=Coord(10,10),
                 visible=True,
                 valid_screens=None):
        self.game = game
        self.game.drawables.append(self)

        self.visible = visible
        if img is not None:
            self.img = pygame.transform.scale(img, size.as_tuple)
        else:
            self.img = img
        self.valid_screens = valid_screens

        if isinstance(position, Coord):
            position = position.as_tuple
        if isinstance(size, Coord):
            size = size.as_tuple

        if not isinstance(position, tuple):
            raise TypeError('Position must be a tuple, not {typeof(position)}')
        if not isinstance(size, tuple):
            raise TypeError('Size must be a tuple, not {typeof(position)}')

        self.x = position[0]
        self.y = position[1]
        self.width = size[0]
        self.height = size[1]


    def __eq__(self, other):
        if not isinstance(other, Drawable): return False
        if not super().__eq__(other): return False
        if self.img != other.img: return False
        if self.valid_screens != other.valid_screens: return False
        return True


    @property
    def size(self):
        return Coord(self.width, self.height)

    @size.setter
    def size(self, new_size):
        if isinstance(new_size, Coord):
            new_size = new_size.as_tuple

        self.width = new_size[0]
        self.height = new_size[1]
        self._size = Coord(*new_size)
        if self.img is not None:
            self.img = pygame.transform.scale(self.img, new_size)


    @property
    def position(self):
        return Coord(self.left, self.top)

    @position.setter
    def position(self, new_position):
        if isinstance(new_position, Coord):
            new_position = new_position.as_tuple

        assert new_position[0] > 0 and new_position[1]
        self.left = new_position[0]
        self.right = new_position[1]


    def delete(self):
        if self in self.game.drawables: self.game.drawables.remove(self)


    def __draw__(self, screen):
        if not self.visible: return False
        if self.valid_screens is not None:
            if isinstance(self.valid_screens, Screen):
                if self.game.current_screen != self.valid_screens: return False
            elif isinstance(self.valid_screens, tuple):
                if self.game.current_screen not in self.valid_screens: return False

        if self.img is None:
            pygame.draw.rect(screen, config.game.default_rect_colour, pygame.Rect(*self.position.as_tuple, *self.size.as_tuple))
        else:
            screen.blit(self.img, self)
        return True


class Clickable(Drawable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_click(self):
        pass


class Simulatable(Drawable):
    def __init__(self, *, game,
                 velocity=Velocity(scalar=0, degrees=0),
                 simulating=True,
                 bounce_screen_edges=True,
                 collide=True,
                 name=None,
                 sound=None,
                 **kwargs):
        """
            Parameters:
            - velocity : The initial speed and direction of the object.
            - simulating : Whether or not to simulate movements and collisions.
            - bounce_screen_edges : Whether or not to bounce off the screen edges when simulating.
            - collide : Whether or not to collide with other collidable objects and to call the collide_callback.
        """
        self.game = game
        self.game.simulatables.append(self)

        self.name = name
        self.sound = sound

        self.velocity = velocity

        self.simulating = simulating
        self.bounce_screen_edges = bounce_screen_edges
        self.collide = collide

        super().__init__(game=game, **kwargs)


    def __eq__(self, other):
        if not isinstance(other, Simulatable): return False
        if not super().__eq__(other): return False
        if self.name != other.name: return False
        if self.sound != other.sound: return False
        if self.velocity != other.velocity: return False
        if self.simulating != other.simulating: return False
        if self.bounce_screen_edges != other.bounce_screen_edges: return False
        if self.collide != other.collide: return False
        return True


    def __str__(self):
        if self.name is not None:
            return f'Simulatable-{self.name}'
        else:
            return super().__str__()


    def delete(self):
        if self in self.game.simulatables:
            self.game.simulatables.remove(self)
        super().delete()


    def __move_object_with_velocity__(self):
        self.x += self.velocity.x
        self.y += self.velocity.y


    def __isimulate__(self):
        """Simulates movement and collisions by modifying self.
        Returns False if nothing was simulated, True if any simulation occurred.
        """
        if not self.simulating: return False
        if self.valid_screens is not None:
            if isinstance(self.valid_screens, Screen):
                if self.game.current_screen != self.valid_screens: return False
            elif isinstance(self.valid_screens, tuple):
                if self.game.current_screen not in self.valid_screens: return False

        self.__move_object_with_velocity__()

        if self.bounce_screen_edges:
            self.__bounce_screen_edges__()

        self.__detect_collisions_with_objects__()

        return True


    def __bounce_screen_edges__(self):
        if self.left <= 0:
            self.velocity.x = abs(self.velocity.x)
            self.screen_edge_callback('left')
        elif self.right >= config.window.size[0]:
            self.velocity.x = -abs(self.velocity.x)
            self.screen_edge_callback('right')


    def __collide_object__(self, obj):
        if self.collide_callback is not None:
            self.collide_callback(obj)
        if obj.collide_callback is not None:
            obj.collide_callback(self)


    def __detect_collisions_with_objects__(self):
        for obj in self.game.collidable_objects():
            if obj == self: continue
            if self.colliderect(obj):
                self.__collide_object__(obj)


    def hit_by_bullet(self, bullet):
        """Doesn't do anything for simulatables, must be implemented for each game_object
        that inherits from this class."""
        pass


    def screen_edge_callback(self, side_bounced_off):
        log.debug(f'I ({self}) bounced off the {side_bounced_off} side.')


    def collide_callback(self, obj):
        log.debug(f'I ({self} collided with {obj}.')
