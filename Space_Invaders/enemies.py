import config
from game_objects import Enemy


class Frigate(Enemy):
    def __init__(self, **kwargs):
        kwargs['size'] = config.enemy.frigate.size
        kwargs['velocity'] = config.enemy.frigate.speed
        kwargs['img'] = config.enemy.frigate.img
        kwargs['bullet_speed'] = config.enemy.frigate.bullet_speed
        kwargs['fire_chance'] = config.enemy.frigate.fire_chance

        super().__init__(**kwargs)

class Carrier(Enemy):
    def __init__(self, **kwargs):
        kwargs['size'] = config.enemy.one.size
        kwargs['velocity'] = config.enemy.one.speed
        kwargs['img'] = config.enemy.one.img
        kwargs['bullet_speed'] = config.enemy.one.bullet_speed
        kwargs['fire_chance'] = config.enemy.one.fire_chance

        super().__init__(**kwargs)

class Buff(Enemy):
    def __init__(self, **kwargs):
        kwargs['size'] = config.enemy.spaceship.size
        kwargs['velocity'] = config.enemy.spaceship.speed
        kwargs['img'] = config.enemy.spaceship.img
        kwargs['bullet_speed'] = config.enemy.spaceship.bullet_speed
        kwargs['fire_chance'] = config.enemy.spaceship.fire_chance

        super().__init__(**kwargs)
