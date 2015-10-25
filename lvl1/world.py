#
# Write in python 3.4
#

import cocos
import pyglet

GROUND_IMAGE_PATH = r'assets/ground.png'
OBSTACLE_IMAGE_PATH = r'assets/obstacle.png'
GOAL_IMAGE_PATH = r'assets/goal.png'

GROUND = 'ground'
OBSTACLE = 'obstacle'
GOAL = 'goal'

TILE_SIZE = (16, 16)
SCREEN_SIZE = (800, 600)


class DungeonTileSet(cocos.tiles.TileSet):

    def __init__(self):
        super(DungeonTileSet, self).__init__(id=0, properties={})

        ground_image = pyglet.image.load(GROUND_IMAGE_PATH)
        obstacle_image = pyglet.image.load(OBSTACLE_IMAGE_PATH)
        goal_image = pyglet.image.load(GOAL_IMAGE_PATH)

        ground_properties = {'obstacle': False, 'goal': True}
        obstacle_properties = {'obstacle': True, 'goal': True}
        goal_properties = {'obstacle': False, 'goal': True}

        self.add(ground_properties, ground_image, GROUND)
        self.add(obstacle_properties, obstacle_image, OBSTACLE)
        self.add(goal_properties, goal_image, GOAL)


class Dungeon(cocos.tiles.RectMapLayer):

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__cells = []
        self.tileset = DungeonTileSet()

        self.__build()
        self.__apply_tileset()

        super(Dungeon, self).__init__('dungeon', TILE_SIZE[0], TILE_SIZE[1], self.__cells)

    def __build(self):
        self.__cells = []

        for x in range(self.width):
            column = []
            for y in range(self.height):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    column.append(OBSTACLE)
                elif x == 1 and y == self.height - 2:
                    column.append(GOAL)
                else:
                    column.append(GROUND)
            self.__cells.append(column)

    def __apply_tileset(self):
        for x in range(self.width):
            for y in range(self.height):
                self.__cells[x][y] = cocos.tiles.RectCell(
                    x, y, TILE_SIZE[0], TILE_SIZE[1], {}, self.tileset[self.__cells[x][y]])

    def set_view(self, screen_size):

        center = (int(screen_size[0] / 2), int(screen_size[1] / 2))
        dungeon_size = (self.width * TILE_SIZE[0], self.height * TILE_SIZE[1])
        origin = (int(dungeon_size[0] / 2 - center[0]), int(dungeon_size[1] / 2 - center[1]))
        print(origin)
        super(Dungeon, self).set_view(
            origin[0],
            origin[1],
            self.width * TILE_SIZE[0] - origin[0],
            self.height * TILE_SIZE[1] - origin[1])


if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], caption='Level 1')

    # We create a new layer, an instance of HelloWorld
    dungeon = Dungeon(15, 20)
    dungeon.set_view(SCREEN_SIZE)
    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(dungeon)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
