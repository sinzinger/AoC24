import multiprocessing
import time

def count_x_mas_in_chunk(chunk, rows, cols, grid):
    count = 0

    # Function to check if a 3x3 window forms an X-MAS
    def is_x_mas(r, c):
        if r - 1 < 0 or r + 1 >= rows or c - 1 < 0 or c + 1 >= cols:
            return False

        # Check the diagonals
        top_left = grid[r - 1][c - 1] + grid[r][c] + grid[r + 1][c + 1]
        bottom_left = grid[r - 1][c + 1] + grid[r][c] + grid[r + 1][c - 1]

        return top_left in {"MAS", "SAM"} and bottom_left in {"MAS", "SAM"}

    # Process the assigned rows in the chunk
    for r in chunk:
        for c in range(1, cols - 1):
            if grid[r][c] == "A" and is_x_mas(r, c):
                count += 1

    return count


def parallel_count_x_mas(grid):
    rows, cols = len(grid), len(grid[0])
    num_processes = multiprocessing.cpu_count()  # Use all available CPUs
    print(num_processes)
    chunk_size = rows // num_processes  # Divide rows into chunks

    # Divide the rows into chunks for each process
    chunks = [range(i * chunk_size, (i + 1) * chunk_size if i < num_processes - 1 else rows)
              for i in range(num_processes)]

    with multiprocessing.Pool(num_processes) as pool:
        results = pool.starmap(count_x_mas_in_chunk, [(chunk, rows, cols, grid) for chunk in chunks])

    return sum(results)

def benchmark(func):
    start_time = time.time()
    result = func()
    end_time = time.time()
    return result, end_time - start_time

def solve_by_multiprocessing():
    file_path = "day_04_input.txt"
    with open(file_path, 'r') as file:
        word_search = file.read().splitlines()

    # Convert the input to a grid of characters
    grid = [list(row) for row in word_search]

    # Count X-MAS patterns using parallel processing
    return parallel_count_x_mas(grid)

if __name__ == "__main__":
    result, benchmarked_time = benchmark(solve_by_multiprocessing)
    print(f"Result = {result}, Time = {benchmarked_time:.4f} seconds")