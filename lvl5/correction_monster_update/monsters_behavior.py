import random


def monster_update(monsters_list):

    # premier monster
    monster_1 = monsters_list[0]

    rnd = random.randint(1, 4)

    if rnd == 1:
        monster_1.right()
    elif rnd == 2:
        monster_1.left()
    elif rnd == 3:
        monster_1.down()
    else:
        monster_1.up()

    # autre monstre
    monsters = monsters_list[1:]
    for monster in monsters:

        hero_position = monster.dungeon.hero_position
        monster_position = monster.dungeon_position

        # axe des x

        if hero_position[0] != monster_position[0]:
            if monster_position[0] < hero_position[0]:
                monster.right()
            else:
                monster.left()
        elif hero_position[1] != monster_position[1]:
            if monster_position[1] < hero_position[1]:
                monster.up()
            else:
                monster.down()
