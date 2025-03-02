from Enemy import *
from Zombie import *
from Ogre import *


def battle(e: Enemy):
    e.talk()
    e.attach()


zombie = Enemy('Zombie', 1 , 10)

big_zomebie = Enemy('Big Zombie', 10.,100)

zombile1 = Zombie('zombie', 10,1)

# ogre = Ogre(20,1)
# # zombie.type_of_enemy = 'Zombie'
# print(zombile1.talk())
# print(ogre.talk())

battle(zombie)
