_This project has been created as part of the 42 curriculum by msuizu, pravet_

**--- Description ---**

a_maze_ing is a program in python >3.10 that generates a maze based on a configuration file.\
when executed, it will display the maze with some user interactions like regenerate a new maze,
show/hide the shortest path, change wall colors ect.\
an output file is also created with inside the maze in hexadecimal values,
the entry and exit position, \
and the shortest path between them with 'N', 'E', 'S' or 'W' caracters.

**--- Instructions ---**

easy execution:
`python3 a_maze_ing.py config.txt`

or with makefile:

`make install`	: install requirements

`make run`	: execute the main script

`make debug`	: run the script in debug mode

`make clean`	: remove temporary files or caches

`make lint`	: execute flake8 and mypy

`make lint-strict`	: execute flake8 and mypy in strict mode

**--- Resources ---**

[display method](https://www.youtube.com/watch?v=W4FnZgiIukg)

[dfs](https://en.wikipedia.org/wiki/Depth-first_search)  and  [bfs](https://en.wikipedia.org/wiki/Breadth-first_search)

AI was used for performance improvements

**--- Configuration File ---**

the config file contains the following mandatory keys:

{WIDTH} : the width of the maze \
{HEIGHT} : the height of the maze\
{ENTRY} : position of the entry in the maze in {x, y} format \
{EXIT} : position of the exit (note that coordinates are between {0} and {size - 1}) \
{OUTPUT_FILE} : the name of the output file \
{PERFECT} : generation a maze with only one path available between entry and exit if set to True\

there are also other keys, although the maze can be generated without them:

{SEED} : the seed of the maze in int or str, which means that every maze is reproductible with their seed \
{ANIMATION} : display the maze with an animation

every setting must be one line by one, in format {key}={value} \
#comments are also available

**--- Maze, Algorithm and Features ---**

DFS (Depth-First Search) was used for the maze generation,because it is popular and is similar to\
the BFS (Breadth-First), which was used for the solving part.

an game interface was also added for the bonus part, using termios and tty libraries \
to put terminal into cbreak mode, the aim is to catch user input directly without having to press enter

the MazeGenerator module is reusable by import it, create MazeGenerator object and `maze.generator()` .

**--- Teamwork ---**

algorithm management and parsing was made by _msuizu_. \
_pravet_ was in charge of the maze's display and the user interface.

everything was ok, except for arranging the schedules at first.