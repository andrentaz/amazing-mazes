# Amazing Mazes
A python project to solve mazes using various graph algorithms.

## About
This project is based on the algorithm presented in [Mazesolving](https://github.com/mikepound/mazesolving) repo from Doctor [Mike Pound](https://www.nottingham.ac.uk/biosciences/people/michael.pound). It uses his algorithm to produce the graph (although the implementation is mine) and run different search algorithms in it.

The final result is saved in a file with the maze cells belonging to the output path being colored from blue to red.

## Installing
To install the project, it's recommended to use python's virtual environment. The project runs on `python3`, so please, make sure to install it first. Once you have your python environment ready to go, run this in your terminal:

```bash
# in the projects folder
python3 -m venv <venv_name>
source <venv_name>/bin/activate
pip install -r requirements.txt
```

## Running
To run the project, use the command line to pass the maze, algorithm and the output path:

```bash
python main.py <input_file> <algorithm> <output_file>
```

The input file should be a maze with the following caracteristics:
- file needs to be in png format
- file with only black and white pixels, where black is a wall and white is a path
- the entrance should be in the first row
- the exit should be in the last row

## Examples
Some examples can be found in examples folder
