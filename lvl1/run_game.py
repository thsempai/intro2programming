import world


def main():

    dungeon_size = (5, 5)
    game = world.Game(dungeon_size)
    hero = Game.hero

    # >>> action du hero

    # Trois actions possibles:
    # move (avance), turn_right (tourne à droite), turn left (tourne à gauche)
    # exemple:
    # hero.turn_left()
    # hero.move()

    # <<< action du hero

    game.run()


if __name__ == '__main__':
    main()
