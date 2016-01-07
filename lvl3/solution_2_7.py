import world


def main():
    dungeon_size = (15, 15)
    game = world.Game(dungeon_size)
    hero = game.hero
    world.GAME_UPDATE_FUNCTION = game_update

    # Version avec une boucle.
    

    game.run()


def game_update(hero):
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
