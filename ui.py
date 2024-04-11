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
NOTIFICATION_TIME = 2

CANVAS_SIZE = 450
CANVAS_LOC = [-365, 365]

CREDIT_LOC = [-150, 150]
LEADER_LOC = [150, 300]
LEADER_LIST_LOC = [150, 240]
GAP = 25

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class UI(metaclass=SingletonMeta):
    """
    UI module draw the splash screen, the background grid,
    the notification prompt and buttons
    and it take controls of drawing the leaderboard
    refreshing the current steps, acted as the 
    Front-End of this game
    """
    def __init__(self):
        """
        Function - init
            initialize the turtle drawing object
            encapsule it in the UI module
            register all the shapes in the puzzle dict
        """
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.pen.speed(TURTLE_SPEED)
        self.pen.hideturtle()
        self.register_shape()
        self.credit_id = None

    def link(self):
        # take the reference of controler module
        self.controler = controler.Controler()

    def register_shape(self):
        """
        Function - register_shape
            register all the path from puzzle dict
            encapsule them in the module
        """
        for path in puzzle.SHAPE_PATH_DICT.values():
            self.screen.register_shape(path)

    def splash_screen(self):
        """
        Function - splash_screen
            reveal the splash screen in the interval of SPLASH_TIME
        """
        self.pen.shape(puzzle.SHAPE_PATH_DICT["splash_screen"])
        stamp_id = self.pen.stamp()
        self.pen.penup()
        time.sleep(SPLASH_TIME)
        self.pen.clearstamp(stamp_id)
    
    def notification(self, type: str):
        """
        Function - notification
            prompt all the different types of notification
            the type is a string can map to the path of the notification
        Param - type
            the notification type (eg. file_error)
        """
        self.pen.pu()
        self.pen.goto(NOTIFICATION_LOC)
        self.pen.pd()
        self.pen.shape(puzzle.SHAPE_PATH_DICT[type])
        stamp_id = self.pen.stamp()
        self.pen.pu()
        time.sleep(NOTIFICATION_TIME)
        self.pen.clearstamp(stamp_id)

    def draw_frame(self):
        """
        Function - draw_frame
            draw 3 square frame as the background of the puzzle game
        """
        self.draw_square(SQUARE[0], "black", PEN_SIZE)
        self.draw_square(SQUARE[1], "black", PEN_SIZE)
        self.draw_square(SQUARE[2], "blue", PEN_SIZE)

    def draw_square(self, square: list[int],
                color: str, size: int):
        """
        Function - draw_square
            draw a square implement the turtle object
        Param - square, color, size
        """
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
        self.pen.pu()
    
    def stamp_pic(self, button_type: str, button_loc: list[int]):
        """
        Function - stamp_pic
            this function mainly used to stamp the pictures of buttons
            onto the canvas, with the input of button_type and button_loc
        Param - button_type, button_loc
        """
        self.pen.penup()
        self.pen.goto(button_loc[0], button_loc[1])
        self.pen.pendown()
        self.pen.shape(puzzle.SHAPE_PATH_DICT[button_type])
        self.pen.stamp()
        self.pen.pu()

    def draw_button(self):
        # iteratively draw all of the buttons onto the canvas
        for i in range(len(BUTTON_TYPE)):
            self.stamp_pic(BUTTON_TYPE[i], BUTTON_LOC[i])
    
    def draw_text(self, str: str, loc: list[int], color: str, align_: str, size: int):
        """
        Function - draw_text
            control the turtle object to draw a text on the canvas
        Param - str, loc, color, align_, size
            the parameters of the actual string
        """
        self.pen.penup()
        self.pen.goto(loc)
        self.pen.pencolor(color)
        self.pen.pd()
        self.pen.write(str, align=align_, font=("Arial", size, "normal"))
        self.pen.pu()
    
    def draw_move(self):
        """
        Function - draw_move
            call the clear_text function first to fill current text with blank white
            move the turtle object to draw the current movement from the controler module
        """
        self.clear_text(CLEAR_LOC[0], CLEAR_LOC[1], CLEAR_SIZE)
        self.pen.pu()
        self.pen.goto(MOVE_LOC)
        self.pen.pencolor("black")
        self.pen.pd()
        self.pen.write(str(self.controler.curr_move), align="center", font=("Arial", 24, "normal"))
        self.pen.pu()
    
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
        self.pen.pu()

    def draw_all(self):
        """
        Function - draw_all
            a combination of all the function in UI module
            to give a initialize UI drawing at start of game
        """
        self.draw_frame()
        self.draw_button()
        self.draw_text("Player Moves:", TEXT_LOC, "red", "center", 24)
        self.draw_move()
        self.draw_leader()
    
    def refresh_canvas(self):
        """
        Function - refresh_canvas
            this function will be called when load a new tile map
            clear the text in the step section
            draw the square of background grid again
        """
        self.clear_text(CANVAS_LOC[0], CANVAS_LOC[1], CANVAS_SIZE)
        self.draw_square(SQUARE[0], "black", PEN_SIZE)

    def onclick(self, x, y):
        """
        Function - onclick
            the onclick event handler for the UI section
            this will receive the user input on the
            button click event
        """
        if RESET_LOC[0][0] < x < RESET_LOC[0][1] and \
        RESET_LOC[1][0] < y < RESET_LOC[1][1]:
            self.controler.reset()
        elif LOAD_LOC[0][0] < x < LOAD_LOC[0][1] and \
        LOAD_LOC[1][0] < y < LOAD_LOC[1][1]:
            self.controler.load()
        elif QUIT_LOC[0][0] < x < QUIT_LOC[0][1] and \
        QUIT_LOC[1][0] < y < QUIT_LOC[1][1]:
            self.controler.quit()
    
    def turn_on_credit(self):
        """
        Function - turn_on_credit
            stamp the credit board and this stamp will not disappear
            since the game is terminated
        """
        self.pen.pu()
        self.pen.goto(CREDIT_LOC[0], CREDIT_LOC[1])
        self.pen.pd()
        self.pen.shape(puzzle.SHAPE_PATH_DICT["credits"])
        self.credit_id = self.pen.stamp()
        self.pen.pu()
    
    def draw_leader(self):
        """
        Function - draw_leader
            draw the leaderboard from leader_list storing in the controler
            iterating through every leader in the leaderboard
        """
        sorted_leader = sorted(self.controler.leader_list, key=lambda x: x[0])
        if len(sorted_leader) > 10:
            sorted_leader = sorted_leader[:10]
        self.draw_text("LEADER", LEADER_LOC, "red", "left", 16)

        for idx, leader in enumerate(sorted_leader):
            line = str(leader[0]) + ": " + leader[1]
            self.draw_text(line, [LEADER_LIST_LOC[0], LEADER_LIST_LOC[1] - GAP * idx], "black", "left", 16)