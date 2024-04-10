import turtle
import ui
import tilemap
import controler

def initialize():
    """
    Function - initialize
        Create all singleton object for this game (UI, Tile Map, Controler)
        Call their link function to initialize them to reference each other
    """
    global screen, game_ui, game_map, game_controler

    # create all singleton class / object for this game
    screen = turtle.Screen()
    game_ui = ui.UI()
    game_map = tilemap.TileMap()
    game_controler = controler.Controler()

    # reference / link them with each other
    game_controler.link()
    game_ui.link()
    game_map.link()

def click_handler(x, y):
    """
    Function - click_handler
        Take the parameter passed by user click input
        Pass them to Tile Map and Ui class for specific function
        If click is disable, ignore the click
    Parameter - x and y
        Default parameter passed by turtle screen onclick event
    """
    if game_controler.allow_click:
        game_map.onclick(x, y)
        game_ui.onclick(x, y)

def main():
    """
    Function - main
        Call initialize function and start_game func in controler class
        Take the input of screen onclick event
        Use mainloop() to make whole game keep running
    """
    initialize()
    game_controler.start_game()
    screen.onclick(click_handler)

    turtle.mainloop()

if __name__ == "__main__":
    main()