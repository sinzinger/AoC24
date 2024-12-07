"""
--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
"""

import time

def count_x_mas(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0

    # Function to check if a 3x3 window forms an X-MAS
    def is_x_mas(r, c):
        if r - 1 < 0 or r + 1 >= rows or c - 1 < 0 or c + 1 >= cols:
            return False

        # Check the diagonals
        top_left = grid[r - 1][c - 1] + grid[r][c] + grid[r + 1][c + 1]
        bottom_left = grid[r - 1][c + 1] + grid[r][c] + grid[r + 1][c - 1]

        return (
            top_left in {"MAS", "SAM"} and bottom_left in {"MAS", "SAM"}
        )

    # Iterate over the grid
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if is_x_mas(r, c):
                count += 1

    return count

def solve_by_single_process():
    file_path = "day_04_input.txt"
    with open(file_path, 'r') as file:
        word_search = file.read().splitlines()

    # Convert the input to a grid of characters
    grid = [list(row) for row in word_search]

    # Count X-MAS patterns
    return count_x_mas(grid)

def benchmark(func):
    start_time = time.time()
    result = func()
    end_time = time.time()
    return result, end_time - start_time

if __name__ == "__main__":
    result, benchmarked_time = benchmark(solve_by_single_process)
    print(f"Result = {result}, Time = {benchmarked_time:.4f} seconds")