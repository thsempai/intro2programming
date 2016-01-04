import world


def main():
    # T: je te laisse regarder le dungeon 6, 6 que tu puisses remarquer que le héro
    # ne pourras pas atteindre sa cible
    dungeon_size = (6, 6)
    game = world.Game(dungeon_size)
    game.run()


def game_update(hero):
    # Exemple à supprimer :p
    if hero.is_at_goal():
        print("I DID IT!")
    else:
        if hero.is_tile_free():
            hero.move()
        else:
            hero.turn_left()
            if hero.is_tile_free():
                hero.move()
            else:
                hero.turn_right()
                hero.turn_right()
    pass

if __name__ == '__main__':
    main()
