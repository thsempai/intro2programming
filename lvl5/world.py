#
# Write in python 3.4
#

import cocos
import pyglet

from pyglet.gl import *

from run_game import game_update
from run_game import on_key_press as game_on_key_press
from maze import Maze
from data import TILE_SIZE, SCREEN_SIZE, SCALE_FACTOR, ACTION_TIME

GROUND_IMAGE_PATH = r'assets/ground.png'
OBSTACLE_IMAGE_PATH = r'assets/obstacle.png'
GOAL_IMAGE_PATH = r'assets/goal.png'

GROUND = 'ground'
OBSTACLE = 'obstacle'
MONSTER = 'monster'
GOAL = 'goal'

MONSTER_IDLE = 0.95


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


class Monster(cocos.sprite.Sprite):

    def __init__(self, image_path):
        pyglet.image.load(image_path)
        super().__init__(
            pyglet.image.load(image_path), (0, 0), anchor=(TILE_SIZE[0]/2, -TILE_SIZE[1] / 3))
        self.dungeon = None
        self.__action = None
        self.__actions = []
        self.__current_action = None
        self.position = (0, 0)
        self.dungeon_position = (0, 0)

        self.new_action = None

    def __move(self, move):
        new_position = self.dungeon_position[0] + move[0], self.dungeon_position[1] + move[1]
        if self.dungeon.is_tile_free_monster(new_position):
            if new_position != self.dungeon.hero_position:
                move_by = TILE_SIZE[0] * move[0], TILE_SIZE[1] * move[1]
                action = cocos.actions.MoveBy(move_by, ACTION_TIME)
                self.new_action = action
                self.dungeon_position = \
                    new_position
                self.dungeon.update_monster_position()

    def get_free_direction(self):
        directions = [Direction.north, Direction.south, Direction.west, Direction.east]
        free = []

        for direction in directions:
            position = \
                self.dungeon_position[0] + direction[0], self.dungeon_position[1] + direction[0]
            if self.dungeon.is_tile_free_monster(position):
                if position != self.dungeon.hero_position:
                    free.append(direction)
        return free

    def move_in_direction(self, direction):
        self.__move(direction)

    def up(self):
        self.__move(Direction.north)

    def down(self):
        self.__move(Direction.south)

    def left(self):
        self.__move(Direction.west)

    def right(self):
        self.__move(Direction.east)

    def append_action(self, action):
        if self.__action:
            self.__action = self.__action + action
        else:
            self.__action = action

    def idle(self):
        action = cocos.actions.interval_actions.ScaleTo(MONSTER_IDLE, ACTION_TIME/2)
        action = action + cocos.actions.interval_actions.ScaleTo(1., ACTION_TIME/2)
        self.append_action(action)

    def go(self):
        if self.__action:
            self.do(self.__action)
            self.__action = None

    def update(self):
        pass


class Hero(cocos.sprite.Sprite):

    def __init__(self):
        hero_image = pyglet.image.load(HERO_IMAGES_PATHS[Direction.north])
        super().__init__(hero_image, (0, 0), anchor=(0, -TILE_SIZE[1] / 3))

        self.dungeon = None
        self.sens = Direction.north
        self.__action = None
        self.__actions = []
        self.__current_action = None

        self.__images = []

        self.__moves = {
            Direction.north: cocos.actions.MoveBy((0, TILE_SIZE[1]), ACTION_TIME),
            Direction.south: cocos.actions.MoveBy((0, -TILE_SIZE[1]), ACTION_TIME),
            Direction.west: cocos.actions.MoveBy((-TILE_SIZE[0], 0), ACTION_TIME),
            Direction.east: cocos.actions.MoveBy((TILE_SIZE[0], 0), ACTION_TIME),
        }


    def __append_action(self, action):
        if self.__action:
            self.__action = self.__action + action
        else:
            self.__action = action

    def __change_image(self):
        image = self.__images.pop(0)
        self.image = image

    def __accept_keys(self):
        self.dungeon.accept_key = True

    def is_tile_free(self):
        return self.dungeon.is_tile_free(self.sens)

    def is_at_goal(self):
        return self.dungeon.is_at_goal()

    def move(self):
        print("In hero.move()")
        if self.dungeon.hero_move(self.sens):
            action = self.__moves[self.sens]
            self.__append_action(action)
        self.__append_action(
            cocos.actions.instant_actions.CallFunc(self.__accept_keys))
        game_update(self, self.dungeon.monsters)
        self.dungeon.monsters_moves()

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
        action += cocos.actions.instant_actions.CallFunc(self.__accept_keys)
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
        action += cocos.actions.instant_actions.CallFunc(self.__accept_keys)
        self.__append_action(action)

    def go(self):
        print("  In hero.go()")
        if self.__action:
            print(type(self.__action))
            self.do(self.__action)
            self.__action = None


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

        ground_properties = {'obstacle': False, 'goal': False}
        obstacle_properties = {'obstacle': True, 'goal': False}
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

    def add_monster(self, monster, position):
        self.character_layer.add(monster)
        self.dungeon.add_monster(monster, position)

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
        cocos.director.director.run(self)


class Dungeon(cocos.tiles.RectMapLayer):

    is_event_handler = True

    def __init__(self, dungeon_size):
        self.dungeon_size = dungeon_size

        self.__cells = []
        self.tiles = []
        self.tileset = DungeonTileSet()

        self.__build()
        # self.__build_maze()
        self.__apply_tileset()

        self.hero = None
        self.hero_position = None
        self.monsters = []
        self.monsters_position = []

        self.accept_key = True

        super(Dungeon, self).__init__('dungeon', TILE_SIZE[0], TILE_SIZE[1], self.__cells)

    def update_monster_position(self):
        self.monsters_position = []
        for monster in self.monsters:
            self.monsters_position.append(monster.dungeon_position)

    def monsters_moves(self):
        for monster in self.monsters:
            if monster.new_action:
                monster.append_action(monster.new_action)
                monster.new_action = None
            else:
                monster.idle()
            monster.go()

    def add_monster(self, monster, position):
        self.monsters_position.append(position)
        monster.dungeon_position = position
        monster.position = position[0] * TILE_SIZE[0] + TILE_SIZE[0]/2, position[1] * TILE_SIZE[1]
        self.monsters .append(monster)
        monster.dungeon = self

    def add_hero(self, hero):
        self.hero = hero

        self.hero.position = self.__begin_postion()
        self.hero_position = self.dungeon_size[0] - 2, 1
        hero.dungeon = self

    def __build_maze(self):
        self.__cells = []

        maze = Maze(*self.dungeon_size)
        self.dungeon_size = (maze.size_x, maze.size_y)

        for x in range(self.dungeon_size[0]):
            column = []
            cells_column = []
            for y in range(self.dungeon_size[1]):
                print(x, y)
                if x == 1 and y == self.dungeon_size[1] - 2:
                    column.append(GOAL)
                elif maze.cells[x][y] == 1:
                    column.append(OBSTACLE)
                else:
                    column.append(GROUND)
                cells_column.append(None)

            self.__cells.append(cells_column)
            self.tiles.append(column)

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
                elif (y+x) % 3 == 0 and x % 2 == 0 and x != self.dungeon_size[0] - 2 \
                        or x == 1 and y == self.dungeon_size[1] - 5 and y != 1:
                    column.append(OBSTACLE)
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

    def __monster_in_position(self, position):

        if position in self.monsters_position:
            return True
        return False

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
        elif self.__monster_in_position(new_position):
            return False
        else:
            self.hero_position = new_position
            return True

    def is_tile_free(self, move):
        new_position = self.hero_position[0] + move[0], self.hero_position[1] + move[1]

        if self.__tile_properties(new_position)[OBSTACLE]:
            return False
        elif self.__monster_in_position(new_position):
            return False
        else:
            return True

    def is_tile_free_monster(self, position):

        if self.__tile_properties(position)[OBSTACLE]:
            return False
        elif self.__monster_in_position(position):
            return False
        else:
            return True

    def is_at_goal(self):
        if self.__tile_properties(self.hero_position)[GOAL]:
            return True
        else:
            return False

    def on_key_press (self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift,
            capslock, etc.)
        """

        if self.accept_key:
            game_on_key_press(key, modifiers, self.hero)
            self.accept_key = False
            self.hero.go()
