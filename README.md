# Puzzle-Slider

this is the description of this course project
and this is the desciption of this course project

## Modulization

this game is construct by 4 main modules: Controler, Puzzle, TileMap, UI
these modules are different singleton object communicate with each other

1. [Controler]
Controler take control of the whole game process, storing the current point,
check the win / loss scenario for this game, has direct control to UI user prompt,
communicate with user and deal with their input, write data to leaderboard and error log file

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

## Valid Puzzle Generation

## Leaderboard and Error file

## Git Version Control