"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

"""

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
            break

    return grid, start_pos, start_dir

def simulate_guard_movement(grid, start_pos, start_dir):
    """Simulate the guard's movement and count distinct positions visited."""
    visited_positions = set()
    current_pos = start_pos
    current_dir = start_dir
    rows, cols = len(grid), len(grid[0])

    while True:
        # Mark current position as visited
        visited_positions.add(current_pos)

        # Calculate the next position in the current direction
        dx, dy = DIRECTIONS[current_dir]
        next_pos = (current_pos[0] + dx, current_pos[1] + dy)

        # Check if the next position is within bounds
        if 0 <= next_pos[1] < rows and 0 <= next_pos[0] < cols:
            if grid[next_pos[1]][next_pos[0]] == '.':  # Walkable path
                current_pos = next_pos
                continue
        else:
            # Guard is out of bounds
            break

        # Turn right (90 degrees) if there is an obstacle
        current_dir = TURN_ORDER[(TURN_ORDER.index(current_dir) + 1) % 4]

    return len(visited_positions)

# Parse the input
file_path = "day_06_input.txt"
grid, start_pos, start_dir = parse_input(file_path)

# Simulate the guard's movement and calculate the result
distinct_positions = simulate_guard_movement(grid, start_pos, start_dir)

# Output the result
print("Distinct Positions Visited:", distinct_positions)