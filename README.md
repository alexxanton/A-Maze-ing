*This project has been created as part of the 42 curriculum by aanton-a, slopez-v*

# A-Maze-ing

## Description
A-Maze-ing is a maze generation, solving, and interactive project. It contains visualizations and a Pacman-like game to test your maze running skills!

## Instructions

### Requirements

* Python 3.10+
* Dependencies listed in `requirements.txt`

### Installation

```bash
make install
```

### Execution

You can run the project using:

```bash
make
```

## Resources

* [Maze Generation: Prim's Algorithm – Jamis Buck Blog](https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
* [Maze Generation: Backtracking Algorithm – Jamis Buck Blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
* [Maze Solver: BFS - Medium](https://medium.com/@luthfisauqi17_68455/artificial-intelligence-search-problem-solve-maze-using-breadth-first-search-bfs-algorithm-255139c6e1a3)
* [Maze Generation – Rosetta Code](https://rosettacode.org/wiki/Maze_generation)

### AI Usage

AI tools were used during the development of this project to:

* Assist with understanding and refining maze generation algorithms
* Provide guidance on structuring the project architecture
* Help debug and improve specific parts of the implementation

## Additional info

### Configuration File

The project uses a configuration file (`config.txt`) to define maze generation parameters.

The structure includes:

* Maze dimensions (width and height)
* Selected generation algorithm (Prim or backtracking)
* Entry and exit
* Output file (for automatic evaluation)
* Perfect mazes or mazes with loops and multiple paths

Two generation algorithms were implemented:

* **Prim’s algorithm** - chosen initially for its simplicity and ease of implementation
* **Backtracking** - later added to produce more visually appealing and organic mazes

### Reusability

The `mazegen` package is designed to be reusable. It encapsulates the maze generation logic and can be imported into other projects to:

* Generate mazes independently of the interface
* Plug into different rendering or game systems

### Team & Project Management

#### Team Members & Responsibilities

* **Alex**

  * Interface development
  * Implementation of Prim’s algorithm
  * Maze solving logic

* **Sergio**

  * Implementation of the backtracking algorithm

#### Planning & Workflow

The project followed an iterative development approach:

* Start with a working implementation
* Continuously refine and expand features
* Iterate over design and structure as new requirements emerged

#### What Worked Well

* Multiple algorithms for better experimentation
* Clear separation between generation and interaction layers

#### What Could Be Improved

* Better encapsulation of classes and responsibilities
* Stronger architectural boundaries between modules
* Cleaner abstraction of maze representation

#### Tools Used

* `curses` - for building the terminal-based interactive interface
