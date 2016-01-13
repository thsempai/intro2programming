import world
from pyglet.window import key

MONSTER_IMAGE_PATH = r'assets/monster.png'
PICKUP_IMAGE_PATH = r'assets/pickup.png'


def main():
    dungeon_size = (10, 10)
    game = world.Game(dungeon_size)

    monster = world.Monster(MONSTER_IMAGE_PATH)
    game.add_monster(monster, (1, 2))

    # pickup = world.Pickup(PICKUP_IMAGE_PATH)
    # game.add_pickup(pickup, (3, 5))

    hero = game.hero

    # Votre code ici :)

    game.run()


def game_update(hero, monsters):

    print("Update")

    for monster in monsters:
        monster.right()


def on_key_press(key_pressed, modifiers, hero):
    pass

def on_pickup_grabbed(pickup, hero, monsters):
    pass

if __name__ == '__main__':
    main()
