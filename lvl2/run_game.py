import world


def main():

    dungeon_size = (5, 5)
    game = world.Game(dungeon_size)
    game.run()


def game_update(hero):
    # Exemple à supprimer :p
    # if hero.is_at_goal():
    #     print("I DID IT!")
    # else:
    #     if hero.is_tile_free():
    #         hero.move()
    #     else:
    #         hero.turn_left()
    #         if hero.is_tile_free():
    #             hero.move()
    #         else:
    #             hero.turn_right()
    #             hero.turn_right()
    pass

if __name__ == '__main__':
    main()
