import turtle
import os
import ui

def input_name():
    screen = turtle.Screen()
    return screen.textinput("5001 Puzzle Slide", "Your Name:")

def input_move():
    screen = turtle.Screen()
    return screen.textinput("5001 Puzzle Slide - Moves", 
                            "Enter the number of moves (chances) you want (5-200)?")

def input_file():
    screen = turtle.Screen()
    game_ui = ui.UI()
    current_directory = os.path.dirname(os.path.realpath(__file__))
    puz_list = get_puz_files(current_directory)
    if len(puz_list) > 10:
        game_ui.notification("file_warning")
        puz_list = puz_list[:10]
    statement = "Enter the name of the puzzle you wish to load. Choices are:\n"
    for puz in puz_list:
        statement += puz + "\n"
    return screen.textinput("Load Puzzle", statement)

def get_puz_files(directory):
    puz_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".puz"):
            puz_files.append(filename)
    return puz_files