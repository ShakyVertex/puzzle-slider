import turtle
import puzzle
import controler
import time

SPLASH_TIME = 1
TURTLE_SPEED = 0
SQUARE = [[-360, 360, 420, 420],
          [-360, -130, 150, 700],
          [130, 360, 420, 210]]
PEN_SIZE = 10

BUTTON_TYPE = ["reset_button", "load_button", "quit_button"]
BUTTON_LOC = [[50, -200], [150, -200], [250, -200]]
RESET_LOC = [[10, 90], [-235, -165]]
LOAD_LOC = [[110, 185], [-230, -160]]
QUIT_LOC = [[210, 290], [-225, -175]]

TEXT_LOC = [-220, -220]
MOVE_LOC = [-80, -220]
CLEAR_SIZE = 60
CLEAR_LOC = [-110, -175]

NOTIFICATION_LOC = [0, 100]
NOTIFICATION_TIME = 3

CANVAS_SIZE = 450
CANVAS_LOC = [-365, 365]

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class UI(metaclass=SingletonMeta):
    def __init__(self):
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.pen.speed(TURTLE_SPEED)
        self.pen.hideturtle()
        self.register_shape()

    def link(self):
        self.controler = controler.Controler()

    def register_shape(self):
        for path in puzzle.SHAPE_PATH_DICT.values():
            self.screen.register_shape(path)

    def splash_screen(self):
        self.pen.shape(puzzle.SHAPE_PATH_DICT["splash_screen"])
        stamp_id = self.pen.stamp()
        self.pen.penup()
        time.sleep(SPLASH_TIME)
        self.pen.clearstamp(stamp_id)
    
    def notification(self, type: str):
        self.pen.pu()
        self.pen.goto(NOTIFICATION_LOC)
        self.pen.pd()
        self.pen.shape(puzzle.SHAPE_PATH_DICT[type])
        stamp_id = self.pen.stamp()
        self.pen.pu()
        time.sleep(NOTIFICATION_TIME)
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
    
    def stamp_pic(self, button_type: str, button_loc: list[int]):
        self.pen.penup()
        self.pen.goto(button_loc[0], button_loc[1])
        self.pen.pendown()
        self.pen.shape(puzzle.SHAPE_PATH_DICT[button_type])
        self.pen.stamp()

    def draw_button(self):
        for i in range(len(BUTTON_TYPE)):
            self.stamp_pic(BUTTON_TYPE[i], BUTTON_LOC[i])
    
    def draw_text(self):
        self.pen.penup()
        self.pen.goto(TEXT_LOC)
        self.pen.pencolor("red")
        self.pen.pd()
        self.pen.write(f"Player Moves:", align="center", font=("Arial", 24, "normal"))
    
    def draw_move(self):
        self.clear_text(CLEAR_LOC[0], CLEAR_LOC[1], CLEAR_SIZE)
        self.pen.pu()
        self.pen.goto(MOVE_LOC)
        self.pen.pencolor("black")
        self.pen.pd()
        self.pen.write(str(self.controler.curr_move), align="center", font=("Arial", 24, "normal"))
    
    def clear_text(self, x, y, size):
        # Clear a box area where the text was written
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.color("white")
        self.pen.begin_fill()
        for _ in range(2):
            self.pen.forward(size)
            self.pen.right(90)
            self.pen.forward(size)
            self.pen.right(90)
        self.pen.end_fill()

    def draw_all(self):
        self.draw_frame()
        self.draw_button()
        self.draw_text()
        self.draw_move()
    
    def refresh_canvas(self):
        self.clear_text(CANVAS_LOC[0], CANVAS_LOC[1], CANVAS_SIZE)
        self.draw_square(SQUARE[0], "black", PEN_SIZE)

    def onclick(self, x, y):
        if RESET_LOC[0][0] < x < RESET_LOC[0][1] and \
        RESET_LOC[1][0] < y < RESET_LOC[1][1]:
            self.controler.reset()
        elif LOAD_LOC[0][0] < x < LOAD_LOC[0][1] and \
        LOAD_LOC[1][0] < y < LOAD_LOC[1][1]:
            self.controler.load()
        elif QUIT_LOC[0][0] < x < QUIT_LOC[0][1] and \
        QUIT_LOC[1][0] < y < QUIT_LOC[1][1]:
            self.controler.quit()