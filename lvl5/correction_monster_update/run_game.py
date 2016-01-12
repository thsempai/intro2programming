import world
from monsters_behavior import monster_update

MONSTER_IMAGE_PATH = r'assets/monster.png'
MONSTER_SPECIAL_IMAGE_PATH = r'assets/monster_special.png'

def main():
    dungeon_size = (10, 10)
    game = world.Game(dungeon_size)

    monster_1 = world.Monster(MONSTER_SPECIAL_IMAGE_PATH)
    game.add_monster(monster_1, (1, 2))

    monster_2 = world.Monster(MONSTER_IMAGE_PATH)
    game.add_monster(monster_2, (2, 2))

    monster_3 = world.Monster(MONSTER_IMAGE_PATH)
    game.add_monster(monster_3, (3, 4))

    hero = game.hero

    # Votre code ici :)

    game.run()


def game_update(hero, monsters):

    monster_update(monsters)

    if not hero.is_at_goal():
        hero.turn_left()
        if not hero.is_tile_free():
            hero.turn_right()
            if not hero.is_tile_free():
                hero.turn_right()
        hero.move()

if __name__ == '__main__':
    main()
