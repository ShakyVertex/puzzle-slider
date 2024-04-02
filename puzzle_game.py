import ui
import userprompt as up
import turtle
import button
import tilemap

def initialize():
    global game_ui, game_button, game_map, screen

    game_ui = ui.UI()
    game_button = button.Button()
    game_map = tilemap.TileMap()
    screen = turtle.Screen()

def start_game():
    global player_name, max_move

    # game_ui.splash_screen()
    # player_name = up.input_name()
    # max_move = up.input_move()
    game_ui.draw_frame()
    game_button.draw_button()
    game_map.load_map("fifteen", True)

def click_handler(x, y):
    game_map.onclick(x, y)

def main():
    initialize()
    start_game()
    screen.onscreenclick(click_handler)

    turtle.mainloop()

if __name__ == "__main__":
    main()