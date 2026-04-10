# mazegen (reusable package)

*This package is part of the 42 curriculum project **A-Maze-ing** (authors: aanton-a, slopez-v).*

`mazegen` is the **reusable** module of the project: it encapsulates maze generation logic so it can be installed with `pip` and imported in other Python projects.

This repository also provides a runner (`a_maze_ing.py`) that reads a configuration file (`config.txt`) and uses the installed `mazegen` package to generate a maze.

---

## Description

A-Maze-ing is a maze generation, solving, and interactive project. It contains visualizations and a Pacman-like game to test your maze running skills.

This `mazegen` package contains the **maze generation** layer.

---

## How to run (from this repository)

From the repository root:

```bash
make
```

This will install dependencies, build/install the `mazegen` package, and run:

```bash
python a_maze_ing.py config.txt
```

You can also run:

```bash
make run
```

---

## Configuration file (`config.txt`)

The project uses a configuration file (`config.txt`) to define maze generation parameters.

The configuration typically includes:

- **Maze dimensions**: `width` and `height`
- **Selected generation algorithm**: `prim` or `backtracking`
- **Entry** coordinates (maze start)
- **Exit** coordinates (maze end)
- **Output file** (for automatic evaluation)
- **Perfect** mazes (single unique solution) or **imperfect** mazes (loops / multiple paths)
- **Seed** (optional): to reproduce the same maze generation

> The exact key names and accepted values are defined by the parser included in this repository.
> Use the provided `config.txt` as the reference template.

### Typical workflow

1. Edit `config.txt` to choose size, algorithm, and output file
2. Run:

   ```bash
   make run
   ```

3. Check the generated output file path (as defined inside `config.txt`)

---

## Generation algorithms

Two generation algorithms are implemented:

- **Prim’s algorithm**  
  Chosen initially for its simplicity and ease of implementation.

- **Backtracking algorithm**  
  Added later to produce more visually appealing and organic mazes.

---

## Accessing the generated structure (library usage)

`mazegen` is designed to be reusable. It encapsulates maze generation logic and can be imported into other projects to:

- Generate mazes independently of the interface
- Plug into different rendering or game systems

Minimal import example:

```python
from mazegen import MazeGenerator, MazeConfig
```

> The exact public API depends on what is exported by `mazegen/__init__.py`.

---

## Additional notes

- The maze generator module grants access to the maze structure, but it is not necessarily the same format as the output file.
- Maze solving and interactive visualization exist in the full project; `mazegen` focuses on generation.

---

## Resources

- Maze Generation: Prim's Algorithm – Jamis Buck Blog
- Maze Generation: Backtracking Algorithm – Jamis Buck Blog
- Maze Solver: BFS
- Maze Generation – Rosetta Code

---

## AI Usage

AI tools were used during the development of this project to:

- Assist with understanding and refining maze generation algorithms
- Provide guidance on structuring the project architecture
- Help debug and improve specific parts of the implementation
