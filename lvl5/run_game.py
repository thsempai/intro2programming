import world
from pyglet.window import key as kb

MONSTER_IMAGE_PATH = r'assets/monster.png'


def main():
    dungeon_size = (10, 10)
    game = world.Game(dungeon_size)

    monster = world.Monster(MONSTER_IMAGE_PATH)
    game.add_monster(monster, (1, 2))

    hero = game.hero

    # Votre code ici :)

    game.run()


def game_update(hero, monsters):

    for monster in monsters:
        monster.right()

def on_key_press(key, modifiers, hero):
    if key == kb.UP:
        hero.move()
    elif key == kb.LEFT:
        hero.turn_left()
    elif key == kb.RIGHT:
        hero.turn_right()

if __name__ == '__main__':
    main()
