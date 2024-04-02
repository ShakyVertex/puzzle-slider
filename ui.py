import turtle
import puzzle
import time

SPLASH_TIME = 1
TURTLE_SPEED = 0
SQUARE = [[-360, 360, 420, 420],
          [-360, -130, 150, 700],
          [130, 360, 420, 210]]
PEN_SIZE = 10

class UI:
    def __init__(self):
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.pen.speed(TURTLE_SPEED)
        self.pen.hideturtle()
        
        self.register_shape()

    def register_shape(self):
        for path in puzzle.SHAPE_PATH_DICT.values():
            self.screen.register_shape(path)

    def splash_screen(self):
        self.pen.shape(puzzle.SHAPE_PATH_DICT["splash_screen"])
        stamp_id = self.pen.stamp()
        self.pen.penup()
        time.sleep(SPLASH_TIME)
        self.pen.clearstamp(stamp_id)

    def draw_frame(self):
        self.draw_square(SQUARE[0], "black", PEN_SIZE)
        self.draw_square(SQUARE[1], "black", PEN_SIZE)
        self.draw_square(SQUARE[2], "blue", PEN_SIZE)

    def draw_square(self, square: list[int],
                color: str, size: int):
        # startup setting
        self.pen.color(color)
        self.pen.pensize(size)
        x, y, height, width = square

        # main drawing
        self.pen.pu()
        self.pen.goto(x, y)
        self.pen.pd()
        self.pen.goto(x, y - height)
        self.pen.goto(x + width, y - height)
        self.pen.goto(x + width, y)
        self.pen.goto(x, y)