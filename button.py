import turtle
import puzzle

TURTLE_SPEED = 0
BUTTON_TYPE = ["reset_button", "load_button", "quit_button"]
BUTTON_LOC = [[50, -200], [150, -200], [250, -200]]

class Button:
    def __init__(self):
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.pen.speed(TURTLE_SPEED)
        self.pen.hideturtle()

    def register_shape(self):
        for path in puzzle.SHAPE_PATH_DICT.values():
            self.screen.register_shape(path)

    def stamp_pic(self, button_type: str, button_loc: list[int]):
        self.pen.penup()
        self.pen.goto(button_loc[0], button_loc[1])
        self.pen.pendown()
        self.pen.shape(puzzle.SHAPE_PATH_DICT[button_type])
        self.pen.stamp()

    def draw_button(self):
        for i in range(len(BUTTON_TYPE)):
            self.stamp_pic(BUTTON_TYPE[i], BUTTON_LOC[i])