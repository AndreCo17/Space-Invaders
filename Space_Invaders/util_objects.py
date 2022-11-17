import math
# import config Cannot use config in this file. Config is based on this file
from timeit import default_timer as time
from time import sleep
from enum import Enum, auto
import copy
from pygame import Rect as PyGameRect


class Screen(Enum):
    Welcome = auto()
    Level1 = auto()
    Level2 = auto()
    Level3 = auto()
    GameOver = auto()


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __sub__(self, other):
        if not isinstance(other, Coord):
            raise ValueError('Can only subtract Coords from a Coord')
        return Coord(self.x - other.x, self.y - other.y)


    def __add__(self, other):
        if not isinstance(other, Coord):
            raise ValueError('Can only add Coords from a Coord')
        return Coord(self.x + other.x, self.y + other.y)


    def __abs__(self):
        return Coord(abs(self.x), abs(self.y))


    def __str__(self):
        return f'Coord({self.x}, {self.y})'


    def __repr__(self):
        return self.__str__()


    @property
    def as_tuple(self):
        return (self.x, self.y)


class Rect(PyGameRect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)


class Velocity:
    def __init__(self, *, x_y=None, scalar=None, radians=None, degrees=None):
        if x_y is not None:
            self.from_components(*x_y)
        else:
            self.scalar = scalar

            if radians is not None:
                self.radians = radians
            elif degrees is not None:
                self.radians = math.radians(degrees)


    @property
    def degrees(self):
        return math.degrees(self.radians)


    @property
    def x(self):
        return math.cos(self.radians) * self.scalar


    @x.setter
    def x(self, new_x):
        components = self.components()
        components = (new_x, components[1])
        self.from_components(*components)


    @property
    def y(self):
        return math.sin(self.radians) * self.scalar


    @y.setter
    def y(self, new_y):
        components = self.components()
        components = (components[0], new_y)
        self.from_components(*components)


    def __repr__(self):
        return f"{round(self.scalar,2)} @ {round(self.degrees,2)}°"


    def __str__(self):
        return self.__repr__()


    def flip_x(self):
        components = self.components()
        components = (-components[0], components[1])
        self.from_components(*components)


    def flip_y(self):
        components = self.components()
        components = (components[0], -components[1])
        self.from_components(*components)


    def from_components(self, x, y):
        self.scalar = Velocity.scalar_from_components(x, y)
        self.radians = Velocity.angle_from_components(x, y)


    def components(self):
        return (self.x, self.y)


    @staticmethod
    def scalar_from_components(x, y):
        return math.sqrt(x**2 + y**2)


    @staticmethod
    def angle_from_components(x, y):
        if x == 0:
            radians = math.radians(90)
        else:
            radians = math.atan(y / x)

        match Velocity.quadrant_from_components(x, y):
            case 0: pass
            case 1:
                radians += 1/2 * math.tau # add 180 degrees
            case 2:
                radians += 1/2 * math.tau # add 180 degrees
            case 3:
                radians = math.tau + radians # subtract from 360 degrees
            case other:
                raise ValueError(f"Invalid quadrant returned from Velocity.quadrant_from_components: {other}")
        return radians


    @staticmethod
    def quadrant_from_components(x, y):
        if x >= 0 and y >= 0:
            return 0
        elif x <= 0 and y >= 0:
            return 1
        elif x <= 0 and y <= 0:
            return 2
        elif x >= 0 and y <= 0:
            return 3


class DroppingStack:
    def __init__(self, size):
        self.arr = []
        self.max_size = size


    def put(self, value):
        if len(self.arr) < self.max_size:
            self.arr.append(value)
        else:
            self.arr.pop(0)
            self.arr.append(value)
