SHAPE_PATH_DICT = {"credits": "Resources/credits.gif",
                   "file_error": "Resources/file_error.gif",
                   "file_warning": "Resources/file_warning.gif",
                   "leaderboard_error": "Resources/leaderboard_error.gif",
                   "load_button": "Resources/loadbutton.gif",
                   "lose": "Resources/Lose.gif",
                   "quit": "Resources/quit.gif",
                   "quit_button": "Resources/quitbutton.gif",
                   "quit_msg": "Resources/quitmsg.gif",
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