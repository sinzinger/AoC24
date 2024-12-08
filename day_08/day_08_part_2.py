"""
--- Part Two ---
Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
"""

import numpy as np
import itertools

def parse_input(filename):
    """Parse the input grid into a NumPy array and frequency mapping."""
    with open(filename, 'r') as file:
        grid = np.genfromtxt(file, dtype='str', delimiter=1)
    frequencies = set(char for row in grid for char in row if char != '.')
    freq_coords = {
        freq: [(x, y) for x, row in enumerate(grid) for y, char in enumerate(row) if char == freq]
        for freq in frequencies
    }
    return grid, freq_coords

def calculate_antinodes(freq_coords, grid_shape):
    """Calculate all antinodes for the given frequency coordinates."""
    shapex, shapey = grid_shape
    antinodes = set()

    for freq, coords in freq_coords.items():
        if len(coords) < 2:
            continue  # No antinodes can be formed with fewer than 2 antennas

        for (x1, y1), (x2, y2) in itertools.combinations(coords, 2):
            dx, dy = x2 - x1, y2 - y1

            # Trace forward along the line
            xa, ya = x1, y1
            while 0 <= xa < shapex and 0 <= ya < shapey:
                antinodes.add((xa, ya))
                xa, ya = xa + dx, ya + dy

            # Trace backward along the line
            xa, ya = x1, y1
            while 0 <= xa < shapex and 0 <= ya < shapey:
                antinodes.add((xa, ya))
                xa, ya = xa - dx, ya - dy

    return antinodes

def main(filename):
    grid, freq_coords = parse_input(filename)
    antinodes = calculate_antinodes(freq_coords, grid.shape)
    print(f"Total unique antinodes: {len(antinodes)}")

if __name__ == "__main__":
    main('./day_08/day_08_input.txt')