#
# Write in python 3.4
#

import cocos
import pyglet

GROUND_IMAGE_PATH = r'assets/ground.png'
OBSTACLE_IMAGE_PATH = r'assets/obstacle.png'

GROUND = 'ground'
OBSTACLE = 'obstacle'

TILE_SIZE = 16


class DungeonTileSet(cocos.tiles.TileSet):

    def __init__(self):
        super(DungeonTileSet, self).__init__(id=0, properties={})

        ground_image = pyglet.image.load(GROUND_IMAGE_PATH)
        obstacle_image = pyglet.image.load(OBSTACLE_IMAGE_PATH)

        ground_properties = {'obstacle': False}
        obstacle_properties = {'obstacle': True}

        self.add(ground_properties, ground_image, GROUND)
        self.add(obstacle_properties, obstacle_image, OBSTACLE)


class Dungeon(cocos.tiles.RectMapLayer):

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__cells = []
        self.tileset = DungeonTileSet()

        self.__build()
        self.__apply_tileset()

        super(Dungeon, self).__init__('dungeon', TILE_SIZE, TILE_SIZE, self.__cells)
        self.set_view(0, 0, self.width * TILE_SIZE, self.height * TILE_SIZE)

    def __build(self):
        self.__cells = []

        for x in range(self.width):
            column = []
            for y in range(self.height):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    column.append(OBSTACLE)
                else:
                    column.append(GROUND)
            self.__cells.append(column)

    def __apply_tileset(self):
        for x in range(self.width):
            for y in range(self.height):
                self.__cells[x][y] = cocos.tiles.RectCell(
                    x, y, TILE_SIZE, TILE_SIZE, {}, self.tileset[self.__cells[x][y]])


if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init()

    # We create a new layer, an instance of HelloWorld
    dungeon = Dungeon(10, 12)

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(dungeon)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
