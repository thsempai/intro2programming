import world

MONSTER_IMAGE_PATH = r'assets/monster.png'


def main():
    dungeon_size = (10, 10)
    game = world.Game(dungeon_size)

    monster = world.Monster(MONSTER_IMAGE_PATH)
    game.add_monster(monster, (1,2))

    hero = game.hero

    # Votre code ici :)

    game.run()


def game_update(hero, monsters):

    for monster in monsters:
        monster.right()

    if not hero.is_at_goal():
        hero.turn_left()
        if not hero.is_tile_free():
            hero.turn_right()
            if not hero.is_tile_free():
                hero.turn_right()
        hero.move()

if __name__ == '__main__':
    main()
