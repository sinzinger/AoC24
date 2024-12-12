"""
--- Day 12: Garden Groups ---
Why not search for the Chief Historian near the gardener and his massive farm? There's plenty of food, so The Historians grab something to eat while they search.

You're about to settle near a complex arrangement of garden plots when some Elves ask if you can lend a hand. They'd like to set up fences around each region of garden plots, but they can't figure out how much fence they need to order or how much it will cost. They hand you a map (your puzzle input) of the garden plots.

Each garden plot grows only a single type of plant and is indicated by a single letter on your map. When multiple garden plots are growing the same type of plant and are touching (horizontally or vertically), they form a region. For example:

AAAA
BBCD
BBCC
EEEC
This 4x4 arrangement includes garden plots growing five different types of plants (labeled A, B, C, D, and E), each grouped into their own region.

In order to accurately calculate the cost of the fence around a single region, you need to know that region's area and perimeter.

The area of a region is simply the number of garden plots the region contains. The above map's type A, B, and C plants are each in a region of area 4. The type E plants are in a region of area 3; the type D plants are in a region of area 1.

Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides of garden plots in the region that do not touch another garden plot in the same region. The type A and C plants are each in a region with perimeter 10. The type B and E plants are each in a region with perimeter 8. The lone D plot forms its own region with perimeter 4.

Visually indicating the sides of plots in each region that contribute to the perimeter using - and |, the above map's regions' perimeters are measured as follows:

+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|
+   +   + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+
Plants of the same type can appear in multiple separate regions, and regions can even appear within other regions. For example:

OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
The above map contains five regions, one containing all of the O garden plots, and the other four each containing a single X plot.

The four X regions each have area 1 and perimeter 4. The region containing 21 type O plants is more complicated; in addition to its outer edge contributing a perimeter of 20, its boundary with each X region contributes an additional 4 to its perimeter, for a total perimeter of 36.

Due to "modern" business practices, the price of fence required for a region is found by multiplying that region's area by its perimeter. The total price of fencing all regions on a map is found by adding together the price of fence for every region on the map.

In the first example, region A has price 4 * 10 = 40, region B has price 4 * 8 = 32, region C has price 4 * 10 = 40, region D has price 1 * 4 = 4, and region E has price 3 * 8 = 24. So, the total price for the first example is 140.

In the second example, the region with all of the O plants has price 21 * 36 = 756, and each of the four smaller X regions has price 1 * 4 = 4, for a total price of 772 (756 + 4 + 4 + 4 + 4).

Here's a larger example:

RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
It contains:

A region of R plants with price 12 * 18 = 216.
A region of I plants with price 4 * 8 = 32.
A region of C plants with price 14 * 28 = 392.
A region of F plants with price 10 * 18 = 180.
A region of V plants with price 13 * 20 = 260.
A region of J plants with price 11 * 20 = 220.
A region of C plants with price 1 * 4 = 4.
A region of E plants with price 13 * 18 = 234.
A region of I plants with price 14 * 22 = 308.
A region of M plants with price 5 * 12 = 60.
A region of S plants with price 3 * 8 = 24.
So, it has a total price of 1930.

What is the total price of fencing all regions on your map?
"""

import random
from collections import deque
from colorama import Fore, Style, init

# Initialize colorama
init()

# A palette of colors
COLORS = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
    Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX, 
    Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, 
    Fore.LIGHTCYAN_EX, Fore.WHITE
]

def bfs_with_coloring(grid, visited, start, plant_type, color_map, used_colors):
    """Performs BFS to calculate area and perimeter of a region and assigns a random color."""
    queue = deque([start])
    visited[start[0]][start[1]] = True
    area = 0
    perimeter = 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    # Assign a random color not recently used
    available_colors = [c for c in COLORS if c not in used_colors[-len(COLORS):]]
    region_color = random.choice(available_colors if available_colors else COLORS)
    used_colors.append(region_color)

    while queue:
        y, x = queue.popleft()
        color_map[y][x] = region_color
        area += 1  # Each cell contributes to the area

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if grid[ny][nx] == plant_type and not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((ny, nx))
                elif grid[ny][nx] != plant_type:  # Neighbor is different
                    perimeter += 1
            else:  # Out of bounds
                perimeter += 1
    
    return area, perimeter

def calculate_total_cost_and_coloring(grid):
    """Calculates the total fencing cost and assigns colors for visualization."""
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    color_map = [[None] * len(grid[0]) for _ in range(len(grid))]
    total_cost = 0
    used_colors = []

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not visited[y][x] and grid[y][x] != '.':  # New region found
                plant_type = grid[y][x]
                area, perimeter = bfs_with_coloring(grid, visited, (y, x), plant_type, color_map, used_colors)
                total_cost += area * perimeter

    return total_cost, color_map

def print_colored_map(grid, color_map):
    """Prints the garden map with unique colors for each region."""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color = color_map[y][x] if color_map[y][x] else Fore.RESET
            print(color + grid[y][x] + Style.RESET_ALL, end='')
        print()

def main():
    grid = [list(line.strip()) for line in open('./day_12/day_12_input.txt', 'r').readlines()]
    total_cost, color_map = calculate_total_cost_and_coloring(grid)
    print_colored_map(grid, color_map)
    print(f"\nTotal cost of fencing: {total_cost}")

if __name__ == "__main__":
    main()