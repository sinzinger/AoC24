import copy
from concurrent.futures import ProcessPoolExecutor
import time

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

def simulate_with_obstruction(grid, start_pos, start_dir, obstruction):
    """Simulate the guard's movement with an optional obstruction."""
    visited = set()
    current_pos = start_pos
    current_dir = start_dir
    rows, cols = len(grid), len(grid[0])

    # Modify grid in place to avoid deep copy overhead
    if obstruction:
        grid[obstruction[1]][obstruction[0]] = '#'

    while True:
        # Record the current position and direction
        state = (current_pos, current_dir)
        if state in visited:
            # Loop detected
            if obstruction:
                grid[obstruction[1]][obstruction[0]] = '.'  # Restore the grid
            return True

        visited.add(state)

        # Calculate the next position
        dx, dy = DIRECTIONS[current_dir]
        next_pos = (current_pos[0] + dx, current_pos[1] + dy)

        # Check if the next position is within bounds and walkable
        if 0 <= next_pos[1] < rows and 0 <= next_pos[0] < cols:
            if grid[next_pos[1]][next_pos[0]] == '.':
                current_pos = next_pos
                continue
            elif grid[next_pos[1]][next_pos[0]] == '#':
                # Obstacle encountered, turn right
                current_dir = TURN_ORDER[(TURN_ORDER.index(current_dir) + 1) % 4]
        else:
            # Guard exits the grid
            if obstruction:
                grid[obstruction[1]][obstruction[0]] = '.'  # Restore the grid
            return False  # No loop detected, simulation ends

def simulate_position(pos, grid, start_pos, start_dir):
    """Simulate guard movement for a specific obstruction position."""
    grid_copy = copy.deepcopy(grid)  # Each process gets its own copy
    return simulate_with_obstruction(grid_copy, start_pos, start_dir, obstruction=pos)

def find_obstruction_positions(grid, start_pos, start_dir):
    """Find all positions where an obstruction causes the guard to loop."""
    rows, cols = len(grid), len(grid[0])

    # Gather all candidate positions
    candidate_positions = [
        (x, y)
        for y in range(rows)
        for x in range(cols)
        if grid[y][x] == '.' and (x, y) != start_pos
    ]

    with ProcessPoolExecutor() as executor:
        results = executor.map(
            simulate_position, candidate_positions, 
            [grid] * len(candidate_positions), 
            [start_pos] * len(candidate_positions), 
            [start_dir] * len(candidate_positions)
        )
        valid_positions = sum(results)

    return valid_positions

if __name__ == "__main__":
    start_time = time.time()

    # Parse the input
    file_path = "day_06_input.txt"
    grid, start_pos, start_dir = parse_input(file_path)

    # Find all valid obstruction positions
    valid_positions = find_obstruction_positions(grid, start_pos, start_dir)

    # Output the result
    print("Valid Obstruction Positions:", valid_positions)

    end_time = time.time()  # End timer
    print(f"Execution Time: {end_time - start_time:.4f} seconds")