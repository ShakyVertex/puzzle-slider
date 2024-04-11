"""
userprompt.py
this file containing all the function for
directly prompt info on textbox to let user input
only deal with the input, do not check valid in these function
"""

import turtle
import controler

def input_name():
    """
    Function - input_name
        prompt the user through a window to let them input name
    """
    screen = turtle.Screen()
    return screen.textinput("5001 Puzzle Slide", "Your Name:")

def input_move():
    """
    Function - input_move
        prompt the user through a window to let them input maximum move
        if the user input is valid return the number move
        else return None
    """
    screen = turtle.Screen()
    try:
        user_input = screen.textinput("5001 Puzzle Slide - Moves", 
                            "Enter the number of moves (chances) you want (5-200)?")
        if int(user_input) >= 5 and int(user_input) <= 200 and int(user_input) == float(user_input):
            return int(user_input)
        else:
            return None
    except ValueError:
        return None

def input_file():
    """
    Function - input file
        prompt the user through a window to let them input .puz file name
    """
    screen = turtle.Screen()
    game_controler = controler.Controler()
    statement = "Enter the name of the puzzle you wish to load. Choices are:\n"
    for puz in game_controler.puz_list[:10]:
        statement += puz + "\n"
    return screen.textinput("Load Puzzle", statement)