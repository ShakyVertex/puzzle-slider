import turtle
import puzzle
import controler
import math
from itertools import product

TURTLE_SPEED = 0
MAP_CENTER = [-150, 150]
THUMBNAIL = [300, 340]
TILE_GAP = 5
EFFECT_SIZE = 2
EFFECT_COLOR = "blue"

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class TileMap(metaclass=SingletonMeta):
    def __init__(self):
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.pen.speed(TURTLE_SPEED)
        self.pen.hideturtle()

        self.matrix = None
        self.stamp_dic = {}
    
    def link(self):
        self.puzzle = puzzle.Puzzle()
        self.controler = controler.Controler()

    def register_shape(self, puzzle_dict: str):
        self.puzzle.load_puzzle(puzzle_dict)
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
                self.matrix[i][j] = str(num)
                num += 1
        else:
            pass
    
    def draw_effect(self, start_point, side_length):
        self.pen.pu()
        self.pen.goto(start_point[0], start_point[1])
        self.pen.pensize(EFFECT_SIZE)
        self.pen.pencolor(EFFECT_COLOR)
        self.pen.pd()
        for _ in range(4):
            self.pen.forward(side_length)
            self.pen.right(90)
    
    def stamp_tile(self, matrix_loc: list[int], tile_id: str, effect=False):
        loc = [start_point[0] + (tile_size + TILE_GAP) * (matrix_loc[1] + 1),
                   start_point[1] - (tile_size + TILE_GAP) * (matrix_loc[0] + 1)]
        if effect:
            effect_point = [loc[0] - (tile_size + TILE_GAP) / 2, loc[1] + (tile_size + TILE_GAP) / 2]
            self.draw_effect(effect_point, (tile_size + TILE_GAP))
        self.pen.pu()
        self.pen.goto(loc[0], loc[1])
        self.pen.pd()
        self.pen.shape(self.puzzle.path_dic[tile_id])
        self.stamp_dic[tile_id] = self.pen.stamp()

    def stamp_matrix(self, effect: bool):
        global tile_size, start_point
        tile_size = int(self.puzzle.info['size'])
        start_point = [MAP_CENTER[0] - (side_length + 1) * (tile_size + TILE_GAP) / 2,
                       MAP_CENTER[1] + (side_length + 1) * (tile_size + TILE_GAP) / 2]
        for i, j in product(range(side_length), range(side_length)):
            self.stamp_tile([i, j], self.matrix[i][j], effect)
    
    def stamp_thumbnail(self):
        self.pen.pu()
        self.pen.goto(THUMBNAIL[0], THUMBNAIL[1])
        self.pen.pd()
        self.pen.shape(self.puzzle.path_dic["thumbnail"])
        self.stamp_dic["thumbnail"] = self.pen.stamp()

    def load_map(self, puzzle_dict: str, order: bool):
        self.register_shape(puzzle_dict)
        self.create_matrix(order)
        self.stamp_matrix(True)
        self.stamp_thumbnail()
    
    def refresh_map(self):
        self.create_matrix(True)
        self.clear(False)
        self.stamp_matrix(False)

    def clear(self, clear_thumb: bool):
        if clear_thumb:
            for stamp_id in self.stamp_dic.values():
                self.pen.clearstamp(stamp_id)
        else:
            for key, stamp_id in self.stamp_dic.items():
                if key == "thumbnail":
                    continue
                else:
                    self.pen.clearstamp(stamp_id)
    
    def swap_tile(self, loc_1: list[int], loc_2: list[int]):
        first_tile = self.matrix[loc_1[0]][loc_1[1]]
        second_tile = self.matrix[loc_2[0]][loc_2[1]]
        self.matrix[loc_1[0]][loc_1[1]] = second_tile
        self.matrix[loc_2[0]][loc_2[1]] = first_tile
        self.pen.clearstamp(self.stamp_dic[first_tile])
        self.pen.clearstamp(self.stamp_dic[second_tile])
        self.stamp_tile(loc_1, second_tile)
        self.stamp_tile(loc_2, first_tile)
    
    def push_tile(self, matrix_loc: list[int]):
        blank_tile = self.puzzle.info["number"]
        surround_loc = []
        if matrix_loc[0] + 1 < side_length:
            surround_loc.append([matrix_loc[0] + 1, matrix_loc[1]])
        if matrix_loc[1] + 1 < side_length:
            surround_loc.append([matrix_loc[0], matrix_loc[1] + 1])
        if matrix_loc[0] > 0:
            surround_loc.append([matrix_loc[0] - 1, matrix_loc[1]])
        if matrix_loc[1] > 0:
            surround_loc.append([matrix_loc[0], matrix_loc[1] - 1])
        
        for loc in surround_loc:
            if self.matrix[loc[0]][loc[1]] == blank_tile:
                self.swap_tile(matrix_loc, loc)
                self.controler.add_move()

    def onclick(self, x, y):
        matrix_loc = [((start_point[1] + (tile_size + TILE_GAP) / 2) - y) // (tile_size + TILE_GAP),
                      (x - (start_point[0] - (tile_size + TILE_GAP) / 2)) // (tile_size + TILE_GAP)]
        matrix_loc[0] = int(matrix_loc[0] - 1)
        matrix_loc[1] = int(matrix_loc[1] - 1)
        if -1 < matrix_loc[0] < side_length and -1 < matrix_loc[1] < side_length:
            self.push_tile(matrix_loc)