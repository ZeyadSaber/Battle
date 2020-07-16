from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Black Magic
of = Spell("Of", 10, 100, "black")
a7 = Spell("A7", 15, 150, "black")
fire = Spell("Fire", 20, 200, "black")

# White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Create Items
super_attack = Item("Super Attack", "spell", "deals 400 HP from your enemy", 400)
super_heal = Item("Super Heal", "heal", "heals you 400 HP", 400)
elixer = Item("Elixer", "elixer", "Fully heals HP/MP for one of the party's members", 0)
mega_elixer = Item("Mega Elixer", "mega_elixer", "Fully heals HP/MP for all the party", 0)

# ========================
player_magic = [of, a7, fire, cure, cura]
player_items = [{"item": super_attack, "quantity": 2}, {"item": super_heal, "quantity": 2},
                {"item": elixer, "quantity": 1}, {"item": mega_elixer, "quantity": 1}]

enemy_magic = [of, a7, cura]

# Initialize People
player1 = Person("Saber", 600, 65, 60, 40, player_magic, player_items)
player2 = Person("7amo ", 750, 70, 80, 48, player_magic, player_items)
player3 = Person("Zizo ", 500, 75, 90, 52, player_magic, player_items)

enemy1 = Person("Gomez", 1500, 65, 45, 35, enemy_magic, [])
enemy2 = Person("Butra", 1200, 70, 45, 35, enemy_magic, [])
enemy3 = Person("Kent ", 1000, 80, 45, 35, enemy_magic, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

running = True

while running:
    print("=================")

    print(bcolors.BOLD + "NAME                        HP                                      MP" + bcolors.ENDC)
    Person.show_stats(enemies, players)

    enemy_index = random.randrange(0, len(enemies))
    enemy_target = random.randrange(0, len(players))

    Person.choose_player(players)
    player_index = int(input("Choose your player: ")) - 1

    players[player_index].choose_action()

    player = players[player_index]
    enemy = enemies[enemy_index]

    choice = int(input("Choose action: "))
    enemy_choice = random.randrange(0, 2)

    if enemy_choice == 0:
        enemy_dmg = enemies[enemy_index].generate_damage()
        players[enemy_target].take_damage(enemy_dmg)
    elif enemy_choice == 1:
        if enemy.get_hp() < enemy.get_max_hp() * 0.25:
            spell = enemy.magic[2]
            magic_dmg = spell.generate_damage()
            current_mp = enemy.get_mp()

            if spell.cost > current_mp:
                continue
            enemy.reduce_mp(spell.cost)
            enemy.heal(magic_dmg)
        else:
            attack_choice = random.randrange(0, 2)
            spell = enemy.magic[attack_choice]
            magic_dmg = spell.generate_damage()
            current_mp = enemy.get_mp()

            if spell.cost > current_mp:
                continue
            enemy.reduce_mp(spell.cost)
            players[enemy_target].take_damage(magic_dmg)
    if choice == 1:
        dmg = player.generate_damage()
        player.choose_enemy(enemies)
        chosen_enemy_idx = int(input("Choose Enemy: ")) - 1
        enemies[chosen_enemy_idx].take_damage(dmg)
        if enemies[chosen_enemy_idx].get_hp() == 0:
            del enemies[chosen_enemy_idx]
    elif choice == 2:
        player.choose_magic()
        magic_choice = int(input("Choose magic: ")) - 1
        if magic_choice == -1:
            continue
        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\n" + player.name + " does't have enough mp\n" + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + spell.name + " heals " + str(magic_dmg) + " to your HP." + bcolors.ENDC)
        elif spell.type == "black":
            Person.choose_enemy(enemies)
            enemy_idx = int(input("Choose Enemy: ")) - 1
            enemies[enemy_idx].take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n",spell.name, "deals", magic_dmg, "from " + enemies[enemy_idx].name + "'s HP\n", bcolors.ENDC)
            if enemies[enemy_idx].get_hp() == 0:
                del enemies[enemy_idx]
    elif choice == 3:
        player.choose_item()
        item_choice = int(input("Choose Item: ")) - 1
        if item_choice == -1:
            continue
        item = player.item[item_choice]["item"]
        if player.item[item_choice]["quantity"] == 0:
            print(bcolors.FAIL + "\nYou don't have anymore from this item (" + player.item[item_choice]["item"].name +
                  ")" + bcolors.ENDC)
            continue

        player.item[item_choice]["quantity"] -= 1

        if item.type == "heal":
            player.heal(item.prop)
            print(bcolors.OKBLUE + item.name + " heals " + str(item.prop) + " to " + player.name.replace(" ", "") +
                  "'s HP." + bcolors.ENDC)
        elif item.type == "spell":
            Person.choose_enemy(enemies)
            enemy_idx = int(input("Choose Enemy: ")) - 1
            enemies[enemy_idx].take_damage(item.prop)
            print(bcolors.OKBLUE + "\n",item.name, "deals", item.prop, "from " +
                  enemies[enemy_idx].name.replace(" ", "") + "'s HP\n", bcolors.ENDC)
            if enemies[enemy_idx].get_hp() == 0:
                del enemies[enemy_idx]
        elif item.type == "elixer":
            player.hp = player.max_hp
            player.mp = player.max_mp
            print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP to " + player.name.replace(" ", "") + "\n"
                  + bcolors.ENDC)
        elif item.type == "mega_elixer":
            for player in players:
                player.hp = player.max_hp
                player.mp = player.max_mp
            print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP to your team\n" + bcolors.ENDC)

    if player.get_hp() == 0:
        del players[enemy_target]

    if not enemies:
        print(bcolors.BOLD + bcolors.OKGREEN + "YOU WIN" + bcolors.ENDC)
        running = False

    if not players:
        print(bcolors.BOLD + bcolors.FAIL + "YOU LOSE" + bcolors.ENDC)
        running = False


