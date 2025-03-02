class Enemy:

    # type_of_enemy: str
    # health_points: int = 10
    # attach_damage: int = 1

    # python tu tao constuctor cho ban
    def __init__(self, type_of_enemy, health_points, attach_damage):
        # print('create an enamy')
        self.type_of_enemy = type_of_enemy
        self.health_points = health_points
        self.attach_damage = attach_damage

    def talk(self):
        print(f'I am a {self.type_of_enemy}. Be Prepared to flight' )

    def walk_forward(self): # buoc ve phia truoc
        print(f'{self.type_of_enemy} move closer to you')

    def attach(self):
        print(f'{self.type_of_enemy} attach for {self.attach_damage} dameage')

