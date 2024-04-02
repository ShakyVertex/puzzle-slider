import ui
import userprompt as up
import turtle
import tilemap
import controler

def initialize():
    global game_ui, game_map, screen

    game_ui = ui.UI()
    game_map = tilemap.TileMap()
    screen = turtle.Screen()
    controler.initialize()

def start_game():
    global player_name, max_move

    # game_ui.splash_screen()
    # player_name = up.input_name()
    # controler.max_move = up.input_move()

    game_ui.draw_all()
    game_map.load_map("mario", True)

def click_handler(x, y):
    game_map.onclick(x, y)

def main():
    initialize()
    start_game()
    screen.onscreenclick(click_handler)

    turtle.mainloop()

if __name__ == "__main__":
    main()