#
# Write in python 3.4
#

import cocos
import pyglet

from pyglet.gl import *

GROUND_IMAGE_PATH = r'assets/ground.png'
OBSTACLE_IMAGE_PATH = r'assets/obstacle.png'
GOAL_IMAGE_PATH = r'assets/goal.png'

GROUND = 'ground'
OBSTACLE = 'obstacle'
GOAL = 'goal'

TILE_SIZE = (16, 16)
SCREEN_SIZE = (400, 300)
SCALE_FACTOR = 2
ACTION_TIME = 2.


class Direction(object):
    north = (0, 1)
    south = (0, -1)
    east = (1, 0)
    west = (-1, 0)

HERO_IMAGES_PATHS = {
    Direction.north: r'assets/hero_n.png',
    Direction.south: r'assets/hero_s.png',
    Direction.east: r'assets/hero_e.png',
    Direction.west: r'assets/hero_w.png'}


class Hero(cocos.sprite.Sprite):

    def __init__(self):
        hero_image = pyglet.image.load(HERO_IMAGES_PATHS[Direction.north])
        super().__init__(hero_image, (0, 0), anchor=(0, -TILE_SIZE[1] / 3))

        self.dungeon = None
        self.sens = Direction.north
        self.__action = None

        self.__images = []

    def __append_action(self, action):
        if self.__action:
            self.__action = self.__action + action
        else:
            self.__action = action

    def __change_image(self):
        image = self.__images.pop(0)
        self.image = image

    def move(self):
        if self.dungeon.hero_move(self.sens):
            move_by = self.sens[0] * TILE_SIZE[0], self.sens[1] * TILE_SIZE[1]
            action = cocos.actions.MoveBy(move_by, ACTION_TIME)
            self.__append_action(action)

    def turn_right(self):
        if self.sens == Direction.north:
            self.sens = Direction.east
        elif self.sens == Direction.east:
            self.sens = Direction.south
        elif self.sens == Direction.south:
            self.sens = Direction.west
        else:
            self.sens = Direction.north

        image = pyglet.image.load(HERO_IMAGES_PATHS[self.sens])
        self.__images.append(image)
        action = cocos.actions.instant_actions.CallFunc(self.__change_image)
        self.__append_action(action)

    def turn_left(self):
        if self.sens == Direction.north:
            self.sens = Direction.west
        elif self.sens == Direction.east:
            self.sens = Direction.north
        elif self.sens == Direction.south:
            self.sens = Direction.east
        else:
            self.sens = Direction.south

        image = pyglet.image.load(HERO_IMAGES_PATHS[self.sens])
        self.__images.append(image)
        action = cocos.actions.instant_actions.CallFunc(self.__change_image)
        self.__append_action(action)

    def go(self):
        if self.__action:
            self.do(self.__action)


class DungeonTileSet(cocos.tiles.TileSet):

    def __init__(self):
        super(DungeonTileSet, self).__init__(id=0, properties={})

        ground_image = pyglet.image.load(GROUND_IMAGE_PATH)
        glTexParameteri(ground_image.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(ground_image.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        obstacle_image = pyglet.image.load(OBSTACLE_IMAGE_PATH)
        glTexParameteri(obstacle_image.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(obstacle_image.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        goal_image = pyglet.image.load(GOAL_IMAGE_PATH)
        glTexParameteri(goal_image.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(goal_image.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        ground_properties = {'obstacle': False, 'goal': True}
        obstacle_properties = {'obstacle': True, 'goal': True}
        goal_properties = {'obstacle': False, 'goal': True}

        self.add(ground_properties, ground_image, GROUND)
        self.add(obstacle_properties, obstacle_image, OBSTACLE)
        self.add(goal_properties, goal_image, GOAL)


class Game(cocos.scene.Scene):

    def __init__(self, dungeon_size):
        window = cocos.director.director.init(
            width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], autoscale=True, caption='Level 1')
        window.set_size(SCREEN_SIZE[0]*SCALE_FACTOR, SCREEN_SIZE[1]*SCALE_FACTOR)

        super(Game, self).__init__()
        self.dungeon = Dungeon(dungeon_size)

        # layer initialisation
        self.character_layer = cocos.layer.Layer()
        self.add(self.dungeon)
        self.add(self.character_layer)

        # character initialisation
        self.hero = Hero()
        self.character_layer.add(self.hero)
        self.dungeon.add_hero(self.hero)

    def draw(self, *args, **kwargs):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        super().draw(*args, **kwargs)

    def set_view(self, screen_size):

        self.dungeon.set_view()
        center = (int(screen_size[0] / 2), int(screen_size[1] / 2))
        dungeon_size = self.dungeon.dungeon_size

        origin = (
            center[0] - int(dungeon_size[0] / 2 * TILE_SIZE[0]),
            int(center[1] - dungeon_size[1] / 2 * TILE_SIZE[1]))

        self.position = origin

    def run(self):
        self.set_view(SCREEN_SIZE)
        self.hero.go()
        cocos.director.director.run(self)


class Dungeon(cocos.tiles.RectMapLayer):

    def __init__(self, dungeon_size):
        self.dungeon_size = dungeon_size

        self.__cells = []
        self.tiles = []
        self.tileset = DungeonTileSet()

        self.__build()
        self.__apply_tileset()

        self.hero = None
        self.hero_position = None

        super(Dungeon, self).__init__('dungeon', TILE_SIZE[0], TILE_SIZE[1], self.__cells)

    def add_hero(self, hero):
        self.hero = hero

        self.hero.position = self.__begin_postion()
        self.hero_position = self.dungeon_size[0] - 2, 1
        hero.dungeon = self

    def __build(self):
        self.__cells = []

        for x in range(self.dungeon_size[0]):
            column = []
            cells_column = []
            for y in range(self.dungeon_size[1]):
                if x == 0 or x == self.dungeon_size[0] - 1 \
                        or y == 0 or y == self.dungeon_size[1] - 1:
                    column.append(OBSTACLE)
                elif x == 1 and y == self.dungeon_size[1] - 2:
                    column.append(GOAL)
                else:
                    column.append(GROUND)
                cells_column.append(None)

            self.__cells.append(cells_column)
            self.tiles.append(column)

    def __apply_tileset(self):
        for x in range(self.dungeon_size[0]):
            for y in range(self.dungeon_size[1]):
                self.__cells[x][y] = cocos.tiles.RectCell(
                    x, y, TILE_SIZE[0], TILE_SIZE[1], {}, self.tileset[self.tiles[x][y]])

    def __begin_postion(self):
        x, y = self.dungeon_size[0] - 2, 1
        return x * TILE_SIZE[0], y * TILE_SIZE[1]

    def __tile_properties(self, position):
        x, y = position
        return self.tileset[self.tiles[x][y]].properties

    def set_view(self):

        super(Dungeon, self).set_view(
            0,
            0,
            self.dungeon_size[0] * TILE_SIZE[0],
            self.dungeon_size[1] * TILE_SIZE[1])

    def hero_move(self, move):

        new_position = self.hero_position[0] + move[0], self.hero_position[1] + move[1]
        if self.__tile_properties(new_position)[OBSTACLE]:
            return False

        else:
            self.hero_position = new_position
            return True


if __name__ == '__main__':
    # director init takes the same arguments as pyglet.window

    dungeon_size = (5, 5)
    game = Game(dungeon_size)
    game.hero.move()
    game.hero.turn_left()
    game.hero.move()
    game.hero.move()
    game.hero.move()
    game.hero.turn_right()
    game.hero.move()
    game.run()
