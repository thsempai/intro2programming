import world


def main():

    dungeon_size = (15, 15)
    game = world.Game(dungeon_size)
    hero = game.hero

    # >>> action du hero

    # Trois actions possibles:
    # move (avance), turn_right (tourne à droite), turn left (tourne à gauche)
    # exemple:
    # hero.move()
    # hero.turn_left()

    # <<< action du hero
    hero.turn_left()
    hero.move()
    hero.move()
    hero.move()
    hero.move()
    hero.turn_right()
    hero.move()
    hero.move()
    hero.move()
    hero.move()
    hero.move()
    hero.move()
    hero.move()
    hero.turn_left()
    hero.move()
    hero.move()
    hero.move()
    hero.move()
    hero.turn_right()
    hero.move()
    hero.move()
    hero.move()
    hero.move()
    hero.turn_left()
    hero.move()
    hero.move()
    hero.move()
    hero.move()
    hero.turn_right()
    hero.move()

    game.run()

if __name__ == '__main__':
    main()
