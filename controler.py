import ui

player_name = None
max_move = None
curr_move = 0

def initialize():
    global game_ui
    game_ui = ui.UI()

def add_move():
    global curr_move
    curr_move += 1
    game_ui.draw_move()