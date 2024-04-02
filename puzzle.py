PUZZLE_PATH_DICT = {"luigi": "luigi.puz",
                    "smiley": "smiley.puz",
                    "family": "family.puz",
                    "fifteen": "fifteen.puz",
                    "yoshi": "yoshi.puz",
                    "mario": "mario.puz"}

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

class Puzzle:
    def __init__(self, puzzle_name = None):
        self.path_dic = {}
        self.info = {}
        
        if puzzle_name:
            self.load_puzzle(puzzle_name)
    
    def load_puzzle(self, puzzle_name: str):
        with open(PUZZLE_PATH_DICT[puzzle_name], "r") as file:
            for line in file:
                # Split the line by ":" to separate the key and value
                key, value = line.strip().split(": ", 1)
                # Add the key-value pair to the dictionary
                if key in INFO:
                    self.info[key] = value
                else:
                    self.path_dic[key] = value