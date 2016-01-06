import world


def main():
    dungeon_size = (19, 19)
    game = world.Game(dungeon_size)
    hero = game.hero

    # Version avec une boucle.
    # Il faut commenter le code dans game_update si on veut l'utiliser.
    # for i in range (1000):
    #     if not hero.is_at_goal():
    #         hero.turn_left()
    #         if not hero.is_tile_free():
    #             hero.turn_right()
    #             if not hero.is_tile_free():
    #                 hero.turn_right()
    #         hero.move()

    game.run()


def game_update(hero):
    # ATTENTION : import à checker dans world.py
    if not hero.is_at_goal():
        hero.turn_left()
        if not hero.is_tile_free():
            hero.turn_right()
            if not hero.is_tile_free():
                hero.turn_right()
        hero.move()

    # Au cas où on commente le reste du code...
    pass

if __name__ == '__main__':
    main()
