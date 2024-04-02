import turtle
import puzzle
import math
from itertools import product

TURTLE_SPEED = 0
MAP_CENTER = [-150, 150]

class TileMap:
    def __init__(self):
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.pen.speed(TURTLE_SPEED)
        self.pen.hideturtle()

        self.puzzle = puzzle.Puzzle()
        self.matrix = None
        self.stamp_dic = {}
    
    def load_map(self, puzzle_name: str, order: bool):
        self.register_shape(puzzle_name)
        self.create_matrix(order)
        self.stamp_matrix()

    def register_shape(self, puzzle_name: str):
        self.puzzle.load_puzzle(puzzle_name)
        for path in self.puzzle.path_dic.values():
            self.screen.register_shape(path)
        
    def create_matrix(self, order: bool):
        global number, side_length
        number = int(self.puzzle.info["number"])
        side_length = int(math.sqrt(number))
        if order:
            self.matrix = [[0] * side_length for _ in range(side_length)]
            num = 1
            for i, j in product(range(side_length), range(side_length)):
                self.matrix[i][j] = num
                num += 1
        else:
            pass
    
    def stamp_tile(self, loc: list[int], tile_id: str):
        self.pen.pu()
        self.pen.goto(loc[0], loc[1])
        self.pen.pd()
        self.pen.shape(self.puzzle.path_dic[tile_id])
        self.stamp_dic[tile_id] = self.pen.stamp()

    def stamp_matrix(self):
        global tile_size
        tile_size = int(self.puzzle.info['size'])
        start_point = [MAP_CENTER[0] - (side_length + 1) * tile_size / 2,
                       MAP_CENTER[1] + (side_length + 1) * tile_size / 2]
        for i, j in product(range(side_length), range(side_length)):
            loc = [start_point[0] + tile_size * (j + 1),
                   start_point[1] - tile_size * (i + 1)]
            self.stamp_tile(loc, str(self.matrix[i][j]))