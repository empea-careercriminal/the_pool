import random

class Player(object):
    """Keeps relevant data of player and handles behavior."""
    def __init__(self, name, gender, age, location, items, mount):
        self.name = name
        self.gender = gender
        self.age = age
        self.strength = age * float(random.uniform(1,2))
        self.hitpoints = age * float(random.uniform(1,2))
        self.items = items
        self.mount = mount
        self.location = location

        self.player_dict = {
        1 : self.name,
        2 : self.gender,
        3 : self.age,
        4 : self.strength,
        5 : self.hitpoints,
        6 : self.items,
        7 : self.mount
        }
    
    def enter(self):
        pass

    def move(self):
        pass

    def talk(self):
        pass

    def give_item(self):
        pass

    def take_item(self):
        pass

    def attack(self):
        pass

    def defend(self):
        pass

    def mount_horse(self):
        pass