import turtle

def input_name():
    screen = turtle.Screen()
    return screen.textinput("5001 Puzzle Slide", "Your Name:")

def input_move():
    screen = turtle.Screen()
    return screen.textinput("5001 Puzzle Slide - Moves", 
                            "Enter the number of moves (chances) you want (5-200)?")