# A* Pathfinding Visualizer

A Python implementation of the **A\*** shortest-path algorithm for solving grid-based mazes with obstacles.

The project uses the **Manhattan distance heuristic** to guide the search efficiently from a start node to an end node and reconstruct the optimal path when one exists.

---

## How It Works

A* evaluates nodes using:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the cost from the start node
- `h(n)` is the estimated distance to the goal
- `f(n)` is the total estimated path cost

The implementation maintains an open set for nodes to explore and reconstructs the shortest path after reaching the goal.

---

## Features

- A* shortest-path search
- Manhattan distance heuristic
- Grid and obstacle handling
- Path reconstruction
- Failure handling when no path exists
- Interactive maze visualization

---

## Project Structure

```text
astar-pathfinding-visualizer/
├── maze_solver/
│   ├── a_star.py
│   ├── buttons.py
│   ├── constants.py
│   ├── graph.py
│   ├── main.py
│   ├── maze.py
│   ├── node_type.py
│   └── node.py
├── Report.md
├── requirements.txt
└── README.md
```

---

## Run Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the visualizer:

```bash
python maze_solver/main.py
```

---

## Technologies

```text
Python
A* Search
Graph Algorithms
Pathfinding
Data Structures
```