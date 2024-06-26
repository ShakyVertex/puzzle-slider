# Puzzle-Slider

A game built in python Turtle Graphic, which is an implementation of the propular geometric drawing tools introduced in Logo,
developed by Wall Feurzeig, Seymour Papert and Cynthia Solomon in 1967.

This is a course project, the instructor ask us do not use Turtle Tkinter shell to implement the graphic module.
With the full requirement list on CS 5001 course website of Northeastern University.

## Modulization

this game is construct by 4 main modules: Controler, Puzzle, TileMap, UI. These modules are different singleton object communicate with each other.
When the user run puzzle.game.py, it fires all the modules to start the game, and mainloop() in the main() function to keep turtle program ongoing.

1. [Controler]
Controler take control of the whole game process, storing the current point, 
check the win / loss scenario for this game, has direct control to UI user prompt, 
communicate with user and deal with their input, write data to leaderboard and error log file.

2. [Puzzle]
Database for the game, implement 2 dictionary to store the img path for all tiles and thumbnail 
storing the information like puzzle name, total count of tiles and tile length 
implement a function to check whether the .puz file is valid

3. [TileMap]
Back-End for the game, encapsule a matrix to represent all the tiles location
deal with tile swap and implement a function to check whether the matrix is in 'win' sequence
implement a algorithm to generate valid puzzle matrix sequence (since random matrix has about 50% probability unsolvable)

4. [UI]
Front-End for the game, storing all the location of GameObject drawing on the UI canvas,
turtle object implement here as a 'pen' to draw all the stuff, using turtle 'shape' and 'stamp' function to
implement almost all the visualization

## Graphic Design
The background grid is drawed by simple turtle usage, while all the pictures and are drawed by using turtle.shape and turtle.stamp
Firstly, register the shape by adding the file path of the pic, and use turtle.stamp to fix it onto the canvas.
While turtle.stamp function returns a stamp_id to help us trace the stamp, and if we want to clear it we just call .clearstamp(stamp_id)
So basically I use a dictionary to store all the stamp_id while creating them. 
Furthermore, for the updating of current score, since we don't have some id to trace the text we write on the board,
so when I need to clear the text, I just fill the area with blank white square.

## Valid Puzzle Generation
The algorithm by doing so I search from the internet, here is the website that has the full explanation.
https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
In the TileMap Module, the generate_valid method generate random array loop until it fulfil the requirement, the is_valid method and count_inversion method are used to determine whether the matrix / array is solvable.