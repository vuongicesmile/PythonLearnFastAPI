from Enemy import *

# same enemy
class Zombie(Enemy):

    def __init__(self, type_of_enemy, health_points, attach_damage):
        super().__init__(
            type_of_enemy=type_of_enemy,
            health_points=health_points,
            attach_damage=attach_damage
        )

    def talk(self):
        print('*Grumbling...*')

    def speard_disease(self):
        print('The zombie is trying to spread')