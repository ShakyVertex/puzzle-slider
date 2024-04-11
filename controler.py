import ui
import tilemap
import os
import turtle
import userprompt as up
import logging
import puzzle

# Configure logging
logging.basicConfig(filename='5001_puzzle.err', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Controler(metaclass=SingletonMeta):
    """
    Singleton Controler, Responsible for storing current game progress
    React to Win / Loss scenerio, Take Control of Reset / Load / Exit button
    Take Control of file system, acted as the Back-End of game
    """
    def __init__(self) -> None:
        """
        Function - init
            Set the default player_name / max_move
            initialize the game and create the scenerio
        """
        self.player_name = "dummy"
        self.curr_move = 0
        self.max_move = 100
        self.allow_click = True
        self.puz_list = self.get_puz_files()
        self.leader_list = self.get_leader()

    def link(self):
        """
        Function - link
            link / take reference to other singleton class / object
        """
        self.game_ui = ui.UI()
        self.game_map = tilemap.TileMap()
        self.puzzle = puzzle.Puzzle()

    def get_puz_files(self):
        """
        Function - get_puz_file
            Find all the file end with .puz
            encap them in the controler class dict
        """
        directory = os.path.dirname(os.path.realpath(__file__))
        puz_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".puz"):
                puz_files.append(filename)
        return puz_files
    
    def start_game(self):
        """
        Function - start_game
            Show the splash screen, let user input name / max move
            Can the ui / tile map class to load a random tile map
        """
        self.game_ui.splash_screen()
        self.player_name = up.input_name()
        self.input_max_move()

        self.game_ui.draw_all()
        self.game_map.load_map(self.puz_list[0], False)

    def input_max_move(self):
        while True:
            input_move = up.input_move()
            if input_move:
                self.max_move = input_move
                break

    def add_move(self):
        """
        Function - add_move
            increment current movement steps by 1
            call Ui class to update canvas
            do win check / loss check at this point
        """
        self.curr_move += 1
        self.game_ui.draw_move()

        if self.game_map.win_check():
            self.win()
        elif self.curr_move > self.max_move:
            self.lose()

    def reset(self):
        """
        Function - reset
            refresh tile map, set the current move to 0
            call Ui class to update canvas
        """
        self.game_map.refresh_map()
        self.curr_move = 0
        self.game_ui.draw_move()

    def load(self):
        """
        Function - load
            Load a different tile map by user input .puz file name
            deal with different user input and file error here
        """
        # if the puzlist encap in the class has over 10 puz file, raise error
        if len(self.puz_list) > 10:
            self.game_ui.notification("file_warning")
            logging.error("File Warning!")

        curr_input = up.input_file()
        if curr_input in self.puz_list and self.puzzle.check_valid(curr_input):
            self.load_valid_puz(curr_input)
        elif curr_input:
            # if the input is invalid, the up function will return None
            self.game_ui.notification("file_error")
            logging.error("File Error!")
        else:
            # if the puz file is invalid, following will execute
            self.game_ui.notification("file_error")
            logging.error("File Error!")
    
    def load_valid_puz(self, curr_input: str):
        """
        Function - load_valid_puz
            if the puz file already check by puzzle class
            encapsule the puzzle to controler
            clear the map and remove the border
            update the ui both Tile Map and Thumbnail
        """
        self.curr_puzzle = curr_input
        self.game_map.clear(True)
        self.game_ui.refresh_canvas()
        self.game_map.load_map(self.curr_puzzle, False)

        self.curr_move = 0
        self.game_ui.draw_move()

    def quit(self):
        """
        Function - quit
            let the UI prompt quitmsg notification
            Terminate the turtle program
        """
        self.game_ui.notification("quitmsg")
        turtle.bye()
    
    def win(self):
        """
        Function - win
            disable the user click event
            let the UI prompt winner notification
            let the UI bring credit window
            save grade to local leaderboard file
        """
        if self.allow_click:
            self.allow_click = False
            self.game_ui.notification("winner")
            self.game_ui.turn_on_credit()
            self.save_grade()
    
    def lose(self):
        """
        Function - lose
            disable the user click event
            let the UI prompt lose notification
            let the UI bring credit window
        """
        if self.allow_click:
            self.allow_click = False
            self.game_ui.notification("lose")
            self.game_ui.turn_on_credit()

    def get_leader(self):
        """
        Function - get_leader
            open up the leaderboard.txt file
            read all the valid leader info
            if the file is not found prompt a UI
        """
        try:
            leader_info = []
            with open("leaderboard.txt", "r") as file:
                for line in file:
                    grade, name = line.strip().split(": ", 1)
                    leader_info.append((int(grade), name))
                return leader_info
            
        except FileNotFoundError:
            self.game_ui.notification("leaderboard_error")
            logging.error("Leaderboard Error!")
            return None

    def save_grade(self):
        """
        Function - save_grade
            this function will be called while game in win status
            open the leaderboard.txt
            write a new line with current username and total steps
            if leaderboard.txt not found, prompt a error in UI
        """
        try:
            with open("leaderboard.txt", "a") as file:
                line = str(self.curr_move) + ": " + self.player_name + "\n"
                file.write(line)
        except FileNotFoundError:
            self.game_ui.notification("leaderboard_error")
            logging.error("Leaderboard Error!")