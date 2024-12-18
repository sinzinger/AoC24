"""
--- Day 18: RAM Run ---
You and The Historians look a lot more pixelated than you remember. You're inside a computer at the North Pole!

Just as you're about to check out your surroundings, a program runs up to you. "This region of memory isn't safe! The User misunderstood what a pushdown automaton is and their algorithm is pushing whole bytes down on top of us! Run!"

The algorithm is fast - it's going to cause a byte to fall into your memory space once every nanosecond! Fortunately, you're faster, and by quickly scanning the algorithm, you create a list of which bytes will fall (your puzzle input) in the order they'll land in your memory space.

Your memory space is a two-dimensional grid with coordinates that range from 0 to 70 both horizontally and vertically. However, for the sake of example, suppose you're on a smaller grid with coordinates that range from 0 to 6 and the following list of incoming byte positions:

5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
Each byte position is given as an X,Y coordinate, where X is the distance from the left edge of your memory space and Y is the distance from the top edge of your memory space.

You and The Historians are currently in the top left corner of the memory space (at 0,0) and need to reach the exit in the bottom right corner (at 70,70 in your memory space, but at 6,6 in this example). You'll need to simulate the falling bytes to plan out where it will be safe to run; for now, simulate just the first few bytes falling into your memory space.

As bytes fall into your memory space, they make that coordinate corrupted. Corrupted memory coordinates cannot be entered by you or The Historians, so you'll need to plan your route carefully. You also cannot leave the boundaries of the memory space; your only hope is to reach the exit.

In the above example, if you were to draw the memory space after the first 12 bytes have fallen (using . for safe and # for corrupted), it would look like this:

...#...
..#..#.
....#..
...#..#
..#..#.
.#..#..
#.#....
You can take steps up, down, left, or right. After just 12 bytes have corrupted locations in your memory space, the shortest path from the top left corner to the exit would take 22 steps. Here (marked with O) is one such path:

OO.#OOO
.O#OO#O
.OOO#OO
...#OO#
..#OO#.
.#.O#..
#.#OOOO
Simulate the first kilobyte (1024 bytes) falling onto your memory space. Afterward, what is the minimum number of steps needed to reach the exit?
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def read_corrupted_coordinates(file_path, limit):
    """
    Reads until the `limit` of corrupted coordinates from a file.

    Args:
        file_path (str): Path to the input file.
        limit (int): Maximum number of coordinates to read.

    Returns:
        list of tuple: List of corrupted coordinates as (x, y) tuples.
    """
    corrupted_coordinates = []
    with open(file_path, "r") as file:
        for line in file:
            x, y = map(int, line.strip().split(","))
            corrupted_coordinates.append((x, y))
            if len(corrupted_coordinates) == limit:
                break
    return corrupted_coordinates


def create_grid_with_obstacles(grid_size, corrupted_coordinates):
    """
    Creates a NetworkX grid graph and removes nodes corresponding to obstacles.

    Args:
        grid_size (int): Size of the grid (grid_size x grid_size).
        corrupted_coordinates (list of tuple): List of corrupted coordinates.

    Returns:
        nx.Graph: Grid graph with obstacles (corrupted coordinates) removed.
    """
    grid_graph = nx.grid_2d_graph(grid_size, grid_size)
    for coord in corrupted_coordinates:
        if coord in grid_graph:
            grid_graph.remove_node(coord)
    return grid_graph


def visualize_grid(grid_size, corrupted_coordinates):
    """
    Visualizes the grid with obstacles using matplotlib.

    Args:
        grid_size (int): Size of the grid (grid_size x grid_size).
        corrupted_coordinates (list of tuple): List of corrupted coordinates.
    """
    grid_visual = np.full((grid_size, grid_size), ".", dtype=str)
    for coord in corrupted_coordinates:
        grid_visual[coord[1], coord[0]] = "#"  # Flip coordinates for display

    plt.figure(figsize=(8, 8))
    plt.imshow(grid_visual == "#", cmap="Greys", interpolation="none")
    for (j, i), label in np.ndenumerate(grid_visual):
        plt.text(i, j, label, ha="center", va="center", color="blue" if label == "." else "red")
    plt.title("Grid with Obstacles (Corrupted Bytes)")
    plt.axis("off")
    plt.show()


def find_shortest_path(graph, start, end):
    """
    Finds the shortest path in a grid graph using A*.

    Args:
        graph (nx.Graph): NetworkX grid graph.
        start (tuple): Starting coordinate (x, y).
        end (tuple): Ending coordinate (x, y).

    Returns:
        tuple: The number of steps of the shortest path.
    """
    try:
        shortest_path = nx.astar_path(graph, source=start, target=end)
        return len(shortest_path) - 1
    except nx.NetworkXNoPath:
        return None, float("inf")


def main():
    grid_size = 71
    file_path = "./day_18/day_18_input.txt"
    num_obstacles = 1024

    corrupted_coordinates = read_corrupted_coordinates(file_path, num_obstacles)
    graph = create_grid_with_obstacles(grid_size, corrupted_coordinates)
    visualize_grid(grid_size, corrupted_coordinates)
    
    start = (0, 0)  # Top-left corner
    end = (grid_size - 1, grid_size - 1)  # Bottom-right corner
    path_length = find_shortest_path(graph, start, end)

    print(f"Number of steps: {path_length}")

if __name__ == "__main__":
    main()