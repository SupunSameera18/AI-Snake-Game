# Hungry Nigel

A self-playing Snake game. Instead of a human player, an A* pathfinding
algorithm controls the snake, plotting the shortest safe route to the food
on every step.

## How it works

- The board is a 50x50 grid rendered in a 600x600 pygame window, with a
  score panel underneath showing the snake's current length.
- A handful of grid cells are randomly marked as **blocks** (walls) when the
  game starts, and the snake must path around them.
- Each time the food is eaten, the game runs A* search from the snake's
  head to the food, treating the snake's own body and any blocks as
  obstacles. The result is a queue of moves (`dir_array`) that the snake
  works through one cell per frame.
- Eating the food grows the snake by one segment and spawns a new food
  cell at a random open (non-blocked, non-snake) location, which triggers
  a fresh A* path calculation.
- If the food hasn't been reached yet, the snake advances one cell along
  its planned path and drops its tail segment, keeping its length the same.
- The game runs indefinitely at a fixed speed (12 frames per second) until
  the window is closed.

There is no player input; the game is a visualization of the A* algorithm
solving Snake on its own.

## The A* algorithm

A* (pronounced "A star") is a pathfinding algorithm that finds the
shortest route between two points on a grid while avoiding obstacles.
It works by exploring the grid outward from the start, always expanding
the most promising cell first, instead of blindly checking every cell
like simpler algorithms do.

Each grid cell (each `Spot` in `HungryNigel.py`) tracks three numbers:

- `g`: the exact cost to reach this cell from the start (the snake's head),
  counted in steps taken so far.
- `h`: a heuristic estimate of the remaining distance from this cell to
  the goal (the food), calculated in the code as straight line distance.
- `f`: the total estimated cost of a path through this cell, simply
  `g + h`.

The `getpath()` function implements the search:

1. Two lists are kept: `openSet`, cells that still need to be checked, and
   `closedSet`, cells that have already been fully checked. The search
   starts with only the snake's head in `openSet`.
2. On each loop, the cell in `openSet` with the lowest `f` score is picked
   as `current`. This is the key idea behind A*: it always investigates
   the cell that looks cheapest overall (cost so far plus estimated cost
   remaining) rather than just the nearest one.
3. `current` is moved to `closedSet`, then each of its neighbors is
   examined. A neighbor is skipped if it is already closed, is a wall
   block, or is part of the snake's body. Otherwise its `g`, `h`, and `f`
   scores are calculated (or updated if a cheaper route to it was just
   found), and it is remembered that it was reached via `current` using
   `cameFrom`.
4. This repeats until the food cell itself is popped as `current`.
5. The final path is then rebuilt by walking backward from the food
   through each cell's `cameFrom` link all the way to the snake's head,
   converting each step into a direction (up, down, left, or right) that
   gets queued up in `dir_array`.

Because blocks and the snake's own body are excluded as valid neighbors,
the path A* finds is guaranteed to be both the shortest available route
and one that the snake can safely follow without crashing into anything
that already exists on the board. The algorithm has no way to see the
food that will spawn next, so it cannot plan around trapping itself in
the long run; it only guarantees the best path to the food it can see
right now.

## Controls

None. Just watch it play. Close the window to quit.

## Requirements

- Python 3
- `pygame`
- `numpy`

Install dependencies:

```bash
pip install pygame numpy
```

## Running

```bash
python HungryNigel.py
```
