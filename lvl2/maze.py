# -*- coding: utf-8 -*-

import random


class Maze(object):

    NORTH = (1, 0)
    SOUTH = (-1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

    DIRECTIONS = (NORTH, SOUTH, EAST, WEST)

    START = (1, 1)

    def __init__(self, size_x, size_y):

        if size_x < 3:
            print("WARNING : Cannot generate a maze with a size < 3.")
            print("          Setting horizontal size to 3.")
            size_x = 3

        if size_y < 3:
            print("WARNING : Cannot generate a maze with a size < 3.")
            print("          Setting vertical size to 3.")
            size_y = 3

        if size_x % 2 == 0:
            print("WARNING : Cannot generate a maze with even size.")
            print("          Decreasing horizontal size by 1.")
            size_x -= 1

        if size_y % 2 == 0:
            print("WARNING : Cannot generate a maze with even size.")
            print("          Decreasing vertical size by 1.")
            size_y -= 1

        self.size_x = size_x
        self.size_y = size_y

        self.cells = []
        for y in range(self.size_y):
            self.cells.append([1] * self.size_x)
        self.generate()

    def __repr__(self):
        return "\n".join(("".join(str(x) for x in row)
                          .replace('1', '█')
                          .replace('0', ' ')
                          ) for row in self.cells)

    def generate(self):
        self.cells[self.START[0]][self.START[1]] = 0
        wall_list = []
        self.add_walls_to_list((self.START[0], self.START[1]), wall_list)
        while(wall_list):
            current = random.choice(wall_list)
            direction = current[2]
            if (current[0]+direction[0] <= 0 or
                    current[0]+direction[0] >= self.size_y-1 or
                    current[1]+direction[1] <= 0 or
                    current[1]+direction[1] >= self.size_x-1):
                continue
            if self.cells[current[0]+direction[0]][current[1]+direction[1]] == 1:
                self.cells[current[0]][current[1]] = 0
                self.cells[current[0]+direction[0]][current[1]+direction[1]] = 0
                self.add_walls_to_list((current[0]+direction[0], current[1]+direction[1]), wall_list)

            wall_list.remove(current)

    def add_walls_to_list(self, cell, wall_list):
        walls = [(cell[0]+direction[0],
                  cell[1]+direction[1],
                  direction) for direction in self.DIRECTIONS]

        for wall in walls:
            if (self.cells[wall[0]][wall[1]] == 1 and
                    wall[0] > 0 and
                    wall[1] > 0 and
                    wall[0] < self.size_y-1 and
                    wall[1] < self.size_x-1 and
                    wall not in wall_list):
                wall_list.append(wall)

# print(Maze(21, 21))
