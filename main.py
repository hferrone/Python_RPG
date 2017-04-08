from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")


# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hi_potion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hi_elixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Instantiate people
player_magic = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hi_potion, "quantity": 5},
                {"item": super_potion, "quantity": 5},{"item": elixer, "quantity": 5},
                {"item": hi_elixer, "quantity": 2},{"item": grenade, "quantity": 5}]
enemy_magic = []
enemy_items = []

player1 = Person("Spike:", 1460, 165, 300, 34, player_magic, player_items)
player2 = Person("Jet:  ", 1860, 265, 360, 34, player_magic, player_items)
player3 = Person("Faye: ", 1360, 125, 260, 34, player_magic, player_items)
player4 = Person("Ed:   ", 1060, 100, 160, 34, player_magic, player_items)
players = [player1, player2, player3, player4]

enemy = Person("Vicious", 1200, 70, 245, 25, enemy_magic, enemy_items)


# Battle methods
def player_attack():
    dmg = player.generate_damage()
    enemy.take_damage(dmg)
    print("You attacked for", dmg, "points of damage.")


def enemy_attack():
    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_damage = enemy.generate_damage()
    players[target].take_damage(enemy_damage)
    print("Enemy attacks for", enemy_damage)


def check_for_win_loss():
    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        battleIsRunning = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        battleIsRunning = False


def show_enemy_stats():
    print("------------------------")
    enemy.get_enemy_stats()


battleIsRunning = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while battleIsRunning:
    print("============================")
    print("\n\n")
    print("NAME                  HP                                      MP")

    for player in players:
        player.get_stats()

    print("\n")
    enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            player_attack()

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for player in players:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals" + str(item.prop), "points of damage" + bcolors.ENDC)

    enemy_attack()
    show_enemy_stats()
    check_for_win_loss()
