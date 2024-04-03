import turtle
import controler

def input_name():
    screen = turtle.Screen()
    return screen.textinput("5001 Puzzle Slide", "Your Name:")

def input_move():
    screen = turtle.Screen()
    return int(screen.textinput("5001 Puzzle Slide - Moves", 
                            "Enter the number of moves (chances) you want (5-200)?"))

def input_file():
    screen = turtle.Screen()
    game_controler = controler.Controler()
    statement = "Enter the name of the puzzle you wish to load. Choices are:\n"
    for puz in game_controler.puz_list[:10]:
        statement += puz + "\n"
    return screen.textinput("Load Puzzle", statement)