import turtle
import puzzle
import controler
import math
from itertools import product
import random

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
    """
    TileMap class take control of all the tiles in the map
    responsible for drawing all tiles / tile-effect / thumbnail
    implement a matrix to represent all the tiles
    deal with swap tile and construct / refresh puzzle matrix in this module
    act as Back-End of this game
    """
    def __init__(self):
        """
        Function - init
            encapsule a turtle object as main drawing tool for the Tile Map
            which is used in drawing boxing effect for the TileMap
            create an empty matrix which will represent all the tile
            create an empty dict to store the stamp id
        """
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.pen.speed(TURTLE_SPEED)
        self.pen.hideturtle()

        self.matrix = None
        self.stamp_dic = {}
    
    def link(self):
        """
        Function - link
            initialize the reference to other singleton game module
        """
        self.puzzle = puzzle.Puzzle()
        self.controler = controler.Controler()

    def register_shape(self, puzzle_dict: str):
        """
        Function - register_shape
            call from puzzle database to load all path from puz file
            register all the shape from these path to turtle screen object
        """
        self.puzzle.load_puzzle(puzzle_dict)
        for path in self.puzzle.path_dic.values():
            self.screen.register_shape(path)
        
    def create_matrix(self, order: bool):
        """
        Function - create_matrix
            create matrix which represent the whole tile map
            if the matrix ordered, just create a increment series for it
            otherwise call generate_valid function to generate a solvable random one
        """
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
            self.generate_valid()

    def generate_valid(self):
        """
        Function - generate_valid
            this function use a specific algorithm to generate
            a solvable random matrix for the tile map
            which has full explanation in the design.txt file
        """
        array = [i + 1 for i in range(number)]

        # continue to generate random array loop until it is valid
        while True:
            valid_array = array.copy()
            random.shuffle(valid_array)
            if self.is_valid(valid_array):
                break
        for i in range(number):
            valid_array[i] = str(valid_array[i])

        # use the valid array to generate valid matrix
        valid_matrix = []
        for i in range(0, number, side_length):
            valid_matrix.append(valid_array[i: i + side_length])
        self.matrix = valid_matrix

    def is_valid(self, array: list[int]) -> bool:
        """
        Function - is_valid
            take a array and determine whether it can generate
            a valid, solvable matrix
        """
        inversion = self.count_inversion(array)
        row_of_blank = side_length - array.index(side_length ** 2) // side_length

        if side_length % 2 == 1 and inversion % 2 == 0:
            return True
        if side_length % 2 == 0:
            if row_of_blank % 2 == 0 and inversion % 2 == 1:
                return True
            if row_of_blank % 2 == 1 and inversion % 2 == 0:
                return True
        return False     

    def count_inversion(self, array):
        """
        Function - count_inversion
            count all the inversion of one array
            which is the essential part of the valid-array generating
            algorithm
        """
        result = 0
        len_array = len(array)
        for i in range(len_array - 1):
            for j in range(i + 1, len_array):
                if array[i] == side_length ** 2 or \
                array[j] == side_length ** 2:
                    continue
                if array[i] > array[j]:
                    result += 1
        return result
    
    def draw_effect(self, start_point, side_length):
        """
        Function - draw_effect
            draw the boxing effect when generating every single tile 
            for the Tile Map
        Parameter - start_point , side_length
            two essential param for drawing details
        """
        self.pen.pu()
        self.pen.goto(start_point[0], start_point[1])
        self.pen.pensize(EFFECT_SIZE)
        self.pen.pencolor(EFFECT_COLOR)
        self.pen.pd()
        for _ in range(4):
            self.pen.forward(side_length)
            self.pen.right(90)
        self.pen.pu()
    
    def stamp_tile(self, matrix_loc: list[int], tile_id: str, effect=False):
        """
        Function - stamp_tile
            stamp a tile according to idx in matrix,
            the location is the global param list in the file
            store the stamp id to the stamp id dict when doing the drawing
        Param - matrix_loc, tile_id, effect
            matrix_loc is the location in matrix, tile_id will take the tile_dict
            to generate all the tiles, effect is default to false,
            if effect is true the function will draw boxing effect for each tile
        """
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
        self.pen.pu()

    def stamp_matrix(self, effect: bool):
        """
        Function - stamp_matrix
            this function will iteratively go through every idx point in matrix
            and stamp every tile according to the path root
        Param - effect
            whether the matrix should draw tiles with boxing effect
            for the reset it will not, for the load / initialize it will
        """
        global tile_size, start_point
        tile_size = int(self.puzzle.info['size'])
        start_point = [MAP_CENTER[0] - (side_length + 1) * (tile_size + TILE_GAP) / 2,
                       MAP_CENTER[1] + (side_length + 1) * (tile_size + TILE_GAP) / 2]
        for i, j in product(range(side_length), range(side_length)):
            self.stamp_tile([i, j], self.matrix[i][j], effect)
    
    def stamp_thumbnail(self):
        """
        Function - stamp_thumbnail
            guide the turtle object to the thumbnail loc
            to stamp the thumbnail from the stamp_dic
            storing in the puzzle database
        """
        self.pen.pu()
        self.pen.goto(THUMBNAIL[0], THUMBNAIL[1])
        self.pen.pd()
        self.pen.shape(self.puzzle.path_dic["thumbnail"])
        self.stamp_dic["thumbnail"] = self.pen.stamp()
        self.pen.pu()

    def load_map(self, puzzle_dict: str, order: bool):
        """
        Function - load_map
            combination for a series of method in this class
            to load a map, this method enable boxing effect drawing by default
        """
        self.register_shape(puzzle_dict)
        self.create_matrix(order)
        self.stamp_matrix(True)
        self.stamp_thumbnail()
    
    def refresh_map(self):
        """
        Function - refresh_map
            combination for a series of method in this class
            to refresh the matrix (implement reset button)
            this will create a ordered matrix
            but do not clear the thumbnail by calling clear
            and stamp new tiles without drawing grid / boxing effect again
        """
        self.create_matrix(True)
        self.clear(False)
        self.stamp_matrix(False)

    def clear(self, clear_thumb: bool):
        """
        Function - clear
            clear all the tiles by using their stamp_id
        Param - clear_thumb
            whether clear the thumbnail
        """
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
        """
        Function - swap_tile
            take two matrix loc input and then swap two tiles
            the algorithm of doing so is swap the id in the matrix Back-End
            and them clear these two stamp from the stamp_id in stamp_dict
            drawing the two new stamps to the location by their new loc
        Param - loc_1 , loc_2
            two idx location in matrix for tile swaping
        """
        first_tile = self.matrix[loc_1[0]][loc_1[1]]
        second_tile = self.matrix[loc_2[0]][loc_2[1]]
        self.matrix[loc_1[0]][loc_1[1]] = second_tile
        self.matrix[loc_2[0]][loc_2[1]] = first_tile

        self.pen.clearstamp(self.stamp_dic[first_tile])
        self.pen.clearstamp(self.stamp_dic[second_tile])
        self.stamp_tile(loc_1, second_tile)
        self.stamp_tile(loc_2, first_tile)
    
    def push_tile(self, matrix_loc: list[int]):
        """
        Function - push_tile
            get the valid surround loc idx of matrix from the
            input matrix loc, call the swap function if there
            are blank_tile in the surround loc
        Param - matrix_loc
            the relatively matrix index loc for input
        """
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
        
        # if the blank tile exist in the surround loc, call swap function
        for loc in surround_loc:
            if self.matrix[loc[0]][loc[1]] == blank_tile:
                self.swap_tile(matrix_loc, loc)
                self.controler.add_move()

    def onclick(self, x, y):
        """
        Function - onclick
            the onclick event handler for tile map
            it take the input from the user click
            if the location of click is in the Tile Map area
            call the push_tile function
        Param - x , y
            two param get from the onclick event input
        """
        matrix_loc = [((start_point[1] + (tile_size + TILE_GAP) / 2) - y) // (tile_size + TILE_GAP),
                      (x - (start_point[0] - (tile_size + TILE_GAP) / 2)) // (tile_size + TILE_GAP)]
        matrix_loc[0] = int(matrix_loc[0] - 1)
        matrix_loc[1] = int(matrix_loc[1] - 1)
        if -1 < matrix_loc[0] < side_length and -1 < matrix_loc[1] < side_length:
            self.push_tile(matrix_loc)

    def win_check(self) -> bool:
        """
        Function - win_check
            this function will be called from the controler class
            it will check whether the player 'win' the game by
            checking whether the matrix is in a sequence
        """
        array = []
        for line in self.matrix:
            array.extend(line)
        len_array = len(array)
        for i in range(len_array - 1):
            if int(array[i]) > int(array[i + 1]):
                return False
        return True