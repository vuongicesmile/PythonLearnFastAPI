from Enemy import *

class Ogre(Enemy):
    def __init__(self, health_points, attach_damage):
        super().__init__(
            type_of_enemy='Ogre',
            health_points=health_points,
            attach_damage=attach_damage
        )

    def talk(self):
        print('Ogre run around')