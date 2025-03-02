class Enemy:

    type_of_enemy: str
    health_points: int = 10
    attach_damage: int = 1

    def talk(self):
        print(f'I am a {self.type_of_enemy}. Be Prepared to flight' )

    def walk_forward(self): # buoc ve phia truoc
        print(f'{self.type_of_enemy} move closer to you')

    def attach(self):
        print(f'{self.type_of_enemy} attach for {self.attach_damage} dameage')

