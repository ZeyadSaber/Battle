import random
from classes.magic import Spell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, item):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.max_mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.item = item
        self.actions = ["Attack", "Magic", "Item"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def heal(self, health):
        self.hp += health
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def choose_action(self):
        i = 1
        print("Actions")
        for item in self.actions:
            print("    " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("Magic")
        for item in self.magic:
            print("    " + str(i) + ".", item.name, "(Cost:", str(item.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("Items")
        for item in self.item:
            print("    " + str(i) + ".", item["item"].name, ":",
                  item["item"].desc + "  (x" + str(item["quantity"]) + ")")
            i += 1

    @staticmethod
    def choose_enemy(enemies):
        i = 1
        print(bcolors.BOLD + "Enemies: " + bcolors.ENDC)
        for enemy in enemies:
            print(bcolors.FAIL + "    " + str(i) + "." + enemy.name + bcolors.ENDC)
            i += 1

    @staticmethod
    def show_stats(enemies, players):

        for player in players:
            hp_ticks = ""
            mp_ticks = ""
            current_hp = ""
            current_mp = ""
            hp_string = str(player.hp) + "/" + str(player.max_hp)
            mp_string = str(player.mp) + "/" + str(player.max_mp)
            n = player.hp / player.max_hp * 25
            m = player.mp / player.max_mp * 10
            while n > 0:
                hp_ticks += "█"
                n -= 1
            while len(hp_ticks) < 25:
                hp_ticks += " "
            while m > 0:
                mp_ticks += "█"
                m -= 1
            while len(mp_ticks) < 10:
                mp_ticks += " "
            if len(hp_string) < 9:
                decreased = 9 - len(hp_string)
                while decreased > 0:
                    current_hp += " "
                    decreased -= 1
            current_hp += hp_string
            if len(mp_string) < 5:
                decreased = 5 - len(mp_string)
                while decreased > 0:
                    current_mp += " "
                    decreased -= 1
            current_mp += mp_string
            print("                            _________________________               __________")
            print(bcolors.BOLD + player.name + bcolors.ENDC + "             " + current_hp + "|" + bcolors.OKGREEN
                  + hp_ticks + bcolors.ENDC + "|        " + current_mp + "|" + bcolors.OKBLUE + mp_ticks + bcolors.ENDC
                  + "|")

        print("\n")

        for enemy in enemies:
            hp_ticks = ""
            mp_ticks = ""
            current_hp = ""
            current_mp = ""
            hp_string = str(enemy.hp) + "/" + str(enemy.max_hp)
            mp_string = str(enemy.mp) + "/" + str(enemy.max_mp)
            n = enemy.hp / enemy.max_hp * 25
            m = enemy.mp / enemy.max_mp * 10
            while n > 0:
                hp_ticks += "█"
                n -= 1
            while len(hp_ticks) < 25:
                hp_ticks += " "
            while m > 0:
                mp_ticks += "█"
                m -= 1
            while len(mp_ticks) < 10:
                mp_ticks += " "
            if len(hp_string) < 9:
                decreased = 9 - len(hp_string)
                while decreased > 0:
                    current_hp += " "
                    decreased -= 1
            current_hp += hp_string
            if len(mp_string) < 5:
                decreased = 5 - len(hp_string)
                while decreased > 0:
                    current_mp += " "
                    decreased -= 1
            current_mp += mp_string
            print("                            _________________________               __________")
            print(bcolors.BOLD + enemy.name + bcolors.ENDC + "             " + current_hp + "|" + bcolors.FAIL
                  + hp_ticks + bcolors.ENDC + "|        " + current_mp + "|" + bcolors.FAIL + mp_ticks + bcolors.ENDC
                  + "|")

    @staticmethod
    def choose_player(players):
        i = 1
        print(bcolors.BOLD + "Players: " + bcolors.ENDC)
        for player in players:
            print("    " + bcolors.OKGREEN + str(i) + "." + player.name + bcolors.ENDC)
            i += 1
