import ui
import userprompt as up
import turtle
import tilemap
import controler

def initialize():
    global game_ui, game_map, screen, game_controler

    screen = turtle.Screen()
    game_ui = ui.UI()
    game_map = tilemap.TileMap()
    game_controler = controler.Controler()

    game_controler.link()
    game_ui.link()
    game_map.link()

def click_handler(x, y):
    game_map.onclick(x, y)
    game_ui.onclick(x, y)

def main():
    initialize()
    game_controler.start_game()
    screen.onclick(click_handler)

    turtle.mainloop()

if __name__ == "__main__":
    main()