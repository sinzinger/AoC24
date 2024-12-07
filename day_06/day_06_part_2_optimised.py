import copy
from concurrent.futures import ThreadPoolExecutor

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

    # Place obstruction if provided
    if obstruction:
        grid[obstruction[1]][obstruction[0]] = '#'

    while True:
        # Record the current position and direction
        state = (current_pos, current_dir)
        if state in visited:
            # Loop detected
            if obstruction:
                grid[obstruction[1]][obstruction[0]] = '.'  # Restore the grid
            return True  # Loop detected

        visited.add(state)

        # Calculate the next position
        dx, dy = DIRECTIONS[current_dir]
        next_pos = (current_pos[0] + dx, current_pos[1] + dy)

        # Check if the next position is within bounds
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

def find_candidate_positions(grid, start_pos, start_dir):
    """Find candidate positions near the guard's patrol path."""
    candidate_positions = set()
    visited = set()
    current_pos = start_pos
    current_dir = start_dir
    rows, cols = len(grid), len(grid[0])

    while True:
        state = (current_pos, current_dir)
        if state in visited:
            break  # Loop detected

        visited.add(state)

        # Mark neighboring positions as candidates
        for dx, dy in DIRECTIONS.values():
            neighbor = (current_pos[0] + dx, current_pos[1] + dy)
            if 0 <= neighbor[1] < rows and 0 <= neighbor[0] < cols:
                if grid[neighbor[1]][neighbor[0]] == '.':
                    candidate_positions.add(neighbor)

        # Calculate the next position
        dx, dy = DIRECTIONS[current_dir]
        next_pos = (current_pos[0] + dx, current_pos[1] + dy)

        if 0 <= next_pos[1] < rows and 0 <= next_pos[0] < cols:
            if grid[next_pos[1]][next_pos[0]] == '.':
                current_pos = next_pos
                continue
            elif grid[next_pos[1]][next_pos[0]] == '#':
                current_dir = TURN_ORDER[(TURN_ORDER.index(current_dir) + 1) % 4]
        else:
            break  # Guard exits the grid

    return candidate_positions

def find_obstruction_positions(grid, start_pos, start_dir):
    """Find all positions where an obstruction causes the guard to loop."""
    # Identify candidate positions
    candidate_positions = find_candidate_positions(grid, start_pos, start_dir)
    valid_positions = 0

    def simulate_position(pos):
        return simulate_with_obstruction(grid, start_pos, start_dir, obstruction=pos)

    # Use ThreadPoolExecutor for parallel simulation
    with ThreadPoolExecutor() as executor:
        results = executor.map(simulate_position, candidate_positions)
        valid_positions = sum(results)

    return valid_positions

# Parse the input
file_path = "day_06_input.txt"
grid, start_pos, start_dir = parse_input(file_path)

# Find all valid obstruction positions
valid_positions = find_obstruction_positions(grid, start_pos, start_dir)

# Output the result
print("Valid Obstruction Positions:", valid_positions)