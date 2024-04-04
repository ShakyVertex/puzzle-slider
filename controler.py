import ui
import tilemap
import os
import turtle
import userprompt as up

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Controler(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.player_name = "dummy"
        self.curr_move = 0
        self.max_move = 20
        self.allow_click = True
        self.puz_list = self.get_puz_files()
        self.leader_list = self.get_leader()

    def link(self):
        self.game_ui = ui.UI()
        self.game_map = tilemap.TileMap()

    def get_puz_files(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        puz_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".puz"):
                puz_files.append(filename)
        return puz_files
    
    def start_game(self):
        # self.game_ui.splash_screen()
        # self.player_name = up.input_name()
        # self.max_move = up.input_move()

        self.game_ui.draw_all()
        self.game_map.load_map(self.puz_list[0], False)

    def add_move(self):
        self.curr_move += 1
        self.game_ui.draw_move()

        if self.game_map.win_check():
            self.win()
        elif self.curr_move > self.max_move:
            self.lose()

    def reset(self):
        self.game_ui.turn_off_credit()
        self.game_map.refresh_map()
        self.curr_move = 0
        self.game_ui.draw_move()
        self.allow_click = True

    def load(self):
        if len(self.puz_list) > 10:
            self.game_ui.notification("file_warning")

        curr_input = up.input_file()
        if curr_input in self.puz_list:
            self.curr_puzzle = curr_input
            self.game_ui.turn_off_credit()
            self.game_map.clear(True)
            self.game_ui.refresh_canvas()
            self.game_map.load_map(self.curr_puzzle, False)

            self.curr_move = 0
            self.game_ui.draw_move()
            self.allow_click = True
        elif curr_input:
            self.game_ui.notification("file_error")

    def quit(self):
        self.game_ui.notification("quitmsg")
        turtle.bye()
    
    def win(self):
        self.allow_click = False
        self.game_ui.notification("winner")
        self.game_ui.turn_on_credit()
        self.save_grade()
    
    def lose(self):
        self.allow_click = False
        self.game_ui.notification("lose")
        self.game_ui.turn_on_credit()

    def get_leader(self):
        try:
            leader_info = []
            with open("leaderboard.txt", "r") as file:
                for line in file:
                    grade, name = line.strip().split(": ", 1)
                    leader_info.append((int(grade), name))
                return leader_info
            
        except FileNotFoundError:
            self.game_ui.notification("leaderboard_error")
            return None

    def save_grade(self):
        try:
            with open("leaderboard.txt", "a") as file:
                line = str(self.curr_move) + ": " + self.player_name + "\n"
                file.write(line)
        except FileNotFoundError:
            self.game_ui.notification("leaderboard_error")