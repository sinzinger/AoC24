"""
--- Day 8: Resonant Collinearity ---
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?
"""

import numpy as np
from collections import defaultdict

def parse_input(file_path):
    """Parse the input file into a NumPy array."""
    with open(file_path, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]
    return np.array(grid)

def extract_antennas(grid):
    """Extract antenna positions and their frequencies."""
    antennas = []
    for y, x in np.argwhere(grid != '.'):
        antennas.append((x, y, grid[y, x]))
    return antennas

def find_antinodes(antennas, grid):
    """Find all unique antinodes based on antenna positions."""
    antinodes = set()
    grid_shape = grid.shape

    # Group antennas by frequency
    antennas_by_frequency = defaultdict(list)
    for x, y, freq in antennas:
        antennas_by_frequency[freq].append((x, y))

    # Process each frequency group independently
    for freq, positions in antennas_by_frequency.items():
        positions = np.array(positions)  # Convert to NumPy array for easier calculations

        for i, (x1, y1) in enumerate(positions):
            for x2, y2 in positions[i + 1:]:
                dx, dy = x2 - x1, y2 - y1  # Direction vector

                # Extend in both directions to find antinodes
                ax1, ay1 = x1 - dx, y1 - dy  # Away from antenna 1
                ax2, ay2 = x2 + dx, y2 + dy  # Away from antenna 2

                # Add antinodes to the set (grid validation occurs separately)
                for ax, ay in [(ax1, ay1), (ax2, ay2)]:
                    if 0 <= ax < grid_shape[1] and 0 <= ay < grid_shape[0]:
                        antinodes.add((ax, ay))
    
    return antinodes

def mark_antinode(grid, x, y):
    """Mark an antinode on the grid for visualization, if no antenna exists at that position."""
    if grid[y, x] == '.':
        grid[y, x] = '#'

def main():
    # Load the input file
    input_file = "./day_08/day_08_input.txt"
    grid = parse_input(input_file)
    
    antennas = extract_antennas(grid)
    antinodes = find_antinodes(antennas, grid)
    
    # Filter valid positions for marking on the grid (visualization only)
    for x, y in antinodes:
        if grid[y, x] == '.':  # Only mark if the cell is empty
            mark_antinode(grid, x, y)
    
    # Visualize the grid (optional)
    print("\nGrid with marked antinodes:")
    for row in grid:
        print(''.join(row))

    # Print total unique antinodes (including those coinciding with antennas)
    print(f"Total unique antinodes: {len(antinodes)}")

if __name__ == "__main__":
    main()