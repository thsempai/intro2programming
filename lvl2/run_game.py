import world


def main():
    dungeon_size = (10, 10)
    game = world.Game(dungeon_size)
    hero = game.hero
    world.GAME_UPDATE_FUNCTION = game_update
    
    # Votre code ici :)

    game.run()


def game_update(hero):
    pass

if __name__ == '__main__':
    main()
