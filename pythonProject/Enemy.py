class Enemy:

    # type_of_enemy: str
    # health_points: int = 10
    # attach_damage: int = 1

    # python tu tao constuctor cho ban
    def __init__(self, type_of_enemy, health_points, attach_damage):
        # print('create an enamy')
        self.__type_of_enemy = type_of_enemy # change private to use double undersource
        self.health_points = health_points
        self.attach_damage = attach_damage

    def talk(self):
        print(f'I am a {self.__type_of_enemy}. Be Prepared to flight' )

    def walk_forward(self): # buoc ve phia truoc
        print(f'{self.__type_of_enemy} move closer to you')

    def attach(self):
        print(f'{self.__type_of_enemy} attach for {self.attach_damage} dameage')

    # vi khai bao la private ne khong the get duoc thuoc tinh prviate tu main
    # vi vay can khai bao geteer
    def get_type_of_enemy(self):
        return self.__type_of_enemy


