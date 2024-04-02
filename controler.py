import ui
import tilemap

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Controler(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.player_name = None
        self.curr_puzzle = "mario.puz"
        self.max_move = None
        self.curr_move = 0

    def link(self):
        self.game_ui = ui.UI()
        self.game_map = tilemap.TileMap()

    def add_move(self):
        self.curr_move += 1
        self.game_ui.draw_move()

    def reset(self):
        self.game_map.refresh_map()

    def load(self):
        print("load")

    def quit(self):
        print("quit")