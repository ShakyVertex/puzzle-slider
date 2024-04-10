import math
import os

SHAPE_PATH_DICT = {"credits": "Resources/credits.gif",
                   "file_error": "Resources/file_error.gif",
                   "file_warning": "Resources/file_warning.gif",
                   "leaderboard_error": "Resources/leaderboard_error.gif",
                   "load_button": "Resources/loadbutton.gif",
                   "lose": "Resources/Lose.gif",
                   "quit": "Resources/quit.gif",
                   "quit_button": "Resources/quitbutton.gif",
                   "quitmsg": "Resources/quitmsg.gif",
                   "reset_button": "Resources/resetbutton.gif",
                   "splash_screen": "Resources/splash_screen.gif",
                   "winner": "Resources/winner.gif"}

INFO = ['name', 'number', 'size']

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Puzzle(metaclass=SingletonMeta):
    def __init__(self, puzzle_name = None):
        self.path_dic = {}
        self.info = {}
        
        if puzzle_name:
            self.load_puzzle(puzzle_name)
    
    def load_puzzle(self, puzzle_dict: str):
        with open(puzzle_dict, "r") as file:
            for line in file:
                # Split the line by ":" to separate the key and value
                key, value = line.strip().split(": ", 1)
                # Add the key-value pair to the dictionary
                if key in INFO:
                    self.info[key] = value
                else:
                    self.path_dic[key] = value

    def check_valid(self, puzzle_dict: str):
        name_valid = number_valid = thumb_valid = size_valid = False
        count = 0

        with open(puzzle_dict, "r") as file:
            for line in file:
                # Split the line by ":" to separate the key and value
                key, value = line.strip().split(": ", 1)
                
                # check if name is valid
                if key == "name":
                    if len(value) == 0:
                        return False
                    else:
                        name_valid = True

                # check if the number is valid
                if key == "number":
                    try:
                        total = int(value)
                        if math.sqrt(total) != int(math.sqrt(total)):
                            return False
                        else:
                            number_valid = True
                    except ValueError:
                        return False
                
                # check if the size is valid
                if key == "size":
                    try:
                        if int(value):
                            size_valid = True
                    except ValueError:
                        return False
                
                # check if the thumbnail is valid
                if key == "thumbnail":
                    if os.path.exists(value):
                        thumb_valid = True
                    else:
                        return False
                
                if key != "name" and key != "number" and \
                    key != "thumbnail" and key != "size":
                    # check if all the puzzle tile is valid (count and path)
                    try:
                        if int(key) >= 1 and int(key) <= total:
                            if os.path.exists(value):
                                count += 1
                            else:
                                return False
                    except ValueError:
                        return False
                
        # if all requirement match return True
        if name_valid and number_valid and \
            thumb_valid and size_valid and total == count:
            return True