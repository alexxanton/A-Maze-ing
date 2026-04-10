# mazegen (reusable package)

*This package is part of the 42 curriculum project **A-Maze-ing** (authors: aanton-a, slopez-v).*

`mazegen` is the **reusable** module of the project: it encapsulates maze generation logic so it can be installed with `pip` and imported in other Python projects.

This repository also provides a runner (`a_maze_ing.py`) that reads `config.txt` and uses the installed `mazegen` package.

---

## What this program does

- Reads a configuration file (`config.txt`)
- Generates a maze using the selected algorithm (Prim or Backtracking)
- Supports perfect mazes (single unique path) and imperfect mazes (loops / multiple paths)
- Writes an output file (for evaluation)

---

## Running from this repository (recommended)

From the repository root:

```bash
make
```

This will install dependencies, build/install the `mazegen` package, and run:

```bash
python a_maze_ing.py config.txt
```

You can also run explicitly:

```bash
make run
```

---

## Configuration file (`config.txt`)

Run the program by passing the configuration file:

```bash
python a_maze_ing.py config.txt
```

`config.txt` defines the maze generation parameters, including:

- Maze dimensions (width and height)
- Selected generation algorithm (Prim or backtracking)
- Entry and exit coordinates
- Output file path (for automatic evaluation)
- Perfect mazes or mazes with loops and multiple paths
- Seed (optional): to reproduce the same maze

> The exact accepted keys and format depend on the parser implemented in this repository.
> Use the provided `config.txt` as the reference template.

---

## Generation algorithms

Two generation algorithms are implemented:

- **Prim’s algorithm**: simple and structured mazes
- **Backtracking**: more organic and “natural” looking mazes

---

## Reusability (import in another project)

The maze generation logic is packaged as `mazegen` so it can be reused independently from the interface.

Minimal import example:

```python
from mazegen import MazeGenerator, MazeConfig
```

(Exact public API depends on what is exported by `mazegen/__init__.py`.)

---

## Notes

- This package focuses on maze generation; the interactive UI layer of the repository is separate.
- The output file format is intended to be compatible with the project validator/evaluation.
