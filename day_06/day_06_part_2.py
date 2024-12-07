"""
--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
"""

import copy
import time

start_time = time.time()

# Define the directions and their corresponding movements
DIRECTIONS = {
    'up': (0, -1),
    'right': (1, 0),
    'down': (0, 1),
    'left': (-1, 0)
}
TURN_ORDER = ['up', 'right', 'down', 'left']  # Order of turns (90 degrees right)

def parse_input(file_path):
    """Parse the map input and extract initial state and grid."""
    with open(file_path, "r") as f:
        grid = [list(line.strip()) for line in f.readlines()]

    # Find the starting position and direction
    start_pos = None
    start_dir = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in "^>v<":
                start_pos = (x, y)
                start_dir = {'^': 'up', '>': 'right', 'v': 'down', '<': 'left'}[cell]
                grid[y][x] = '.'  # Replace the starting position with a walkable path
                break
        if start_pos:
            print (start_pos)
            break

    return grid, start_pos, start_dir

def simulate_with_obstruction(grid, start_pos, start_dir, obstruction):
    """Simulate the guard's movement with an optional obstruction."""
    visited = set()
    current_pos = start_pos
    current_dir = start_dir
    rows, cols = len(grid), len(grid[0])

    grid_copy = copy.deepcopy(grid)

    # Place obstruction if provided
    if obstruction:
        grid_copy[obstruction[1]][obstruction[0]] = '#'

    while True:
        # Record the current position and direction
        state = (current_pos, current_dir)
        if state in visited:
            # Loop detected
            return True

        visited.add(state)

        # Calculate the next position
        dx, dy = DIRECTIONS[current_dir]
        next_pos = (current_pos[0] + dx, current_pos[1] + dy)

        # Check if the next position is within bounds and walkable
        if 0 <= next_pos[1] < rows and 0 <= next_pos[0] < cols:
            if grid_copy[next_pos[1]][next_pos[0]] == '.':
                current_pos = next_pos
                continue
            elif grid_copy[next_pos[1]][next_pos[0]] == '#':
                # Obstacle encountered, turn right
                current_dir = TURN_ORDER[(TURN_ORDER.index(current_dir) + 1) % 4]
        else:
            # Guard exits the grid
            return False  # No loop detected, simulation ends

def find_obstruction_positions(grid, start_pos, start_dir):
    """Find all positions where an obstruction causes the guard to loop."""
    rows, cols = len(grid), len(grid[0])
    valid_positions = 0

    # Iterate over all possible positions
    for y in range(rows):
        for x in range(cols):
            # Skip the starting position and non-walkable positions
            if (x, y) == start_pos or grid[y][x] != '.':
                continue

            # Simulate with the obstruction at (x, y)
            if simulate_with_obstruction(grid, start_pos, start_dir, obstruction=(x, y)):
                valid_positions += 1

    return valid_positions

# Parse the input
file_path = "day_06_input.txt" # "day_06_input_from_challenge.txt"
grid, start_pos, start_dir = parse_input(file_path)

# Find all valid obstruction positions
valid_positions = find_obstruction_positions(grid, start_pos, start_dir)

# Output the result
print("Valid Obstruction Positions:", valid_positions)

end_time = time.time()  # End timer
print(f"Execution Time: {end_time - start_time:.4f} seconds")
