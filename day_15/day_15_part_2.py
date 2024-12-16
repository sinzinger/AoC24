"""
--- Part Two ---
The lanternfish use your information to find a safe moment to swim in and turn off the malfunctioning robot! Just as they start preparing a festival in your honor, reports start coming in that a second warehouse's robot is also malfunctioning.

This warehouse's layout is surprisingly similar to the one you just helped. There is one key difference: everything except the robot is twice as wide! The robot's list of movements doesn't change.

To get the wider warehouse's map, start with your original map and, for each tile, make the following changes:

If the tile is #, the new map contains ## instead.
If the tile is O, the new map contains [] instead.
If the tile is ., the new map contains .. instead.
If the tile is @, the new map contains @. instead.
This will produce a new warehouse map which is twice as wide and with wide boxes that are represented by []. (The robot does not change size.)

The larger example from before would now look like this:

####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################
Because boxes are now twice as wide but the robot is still the same size and speed, boxes can be aligned such that they directly push two other boxes at once. For example, consider this situation:

#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
After appropriately resizing this map, the robot would push around these boxes as follows:

Initial state:
##############
##......##..##
##..........##
##....[][]@.##
##....[]....##
##..........##
##############

Move <:
##############
##......##..##
##..........##
##...[][]@..##
##....[]....##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[].@..##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.......@..##
##############

Move <:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##......@...##
##############

Move <:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.....@....##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############

Move <:
##############
##......##..##
##...[][]...##
##....[]....##
##....@.....##
##..........##
##############

Move <:
##############
##......##..##
##...[][]...##
##....[]....##
##...@......##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##...@[]....##
##..........##
##..........##
##############

Move ^:
##############
##...[].##..##
##...@.[]...##
##....[]....##
##..........##
##..........##
##############
This warehouse also uses GPS to locate the boxes. For these larger boxes, distances are measured from the edge of the map to the closest edge of the box in question. So, the box shown below has a distance of 1 from the top edge of the map and 5 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 5 = 105.

##########
##...[]...
##........
In the scaled-up version of the larger example from above, after the robot has finished all of its moves, the warehouse would look like this:

####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..@......[].[][]##
##......[][]..[]..##
####################
The sum of these boxes' GPS coordinates is 9021.

Predict the motion of the robot and boxes in this new, scaled-up warehouse. What is the sum of all boxes' final GPS coordinates?
"""

import numpy as np
from io import StringIO
import time

def load_input(file_path):
    with open(file_path, "r") as f:
        data = f.read().split("\n\n")
    return data[0], data[1].replace("\n", "")


def double_width(grid):
    """
    Transform the initial grid into a warehouse with double width.
    """
    grid = (
        grid.replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
    )
    return np.genfromtxt(
        StringIO(grid), dtype=str, delimiter=1, deletechars="", comments="_",
    )


def print_grid(grid):
    #CLEAR_SCREEN = "\033[2J"
    #MOVE_CURSOR_HOME = "\033[H"
    #print(f"{CLEAR_SCREEN}{MOVE_CURSOR_HOME}", end="")

    LIGHT_BLUE = "\033[94m"
    LIGHT_GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    for row in grid:
        row_output = ""
        for tile in row:
            if tile == "#":
                row_output += f"{LIGHT_BLUE}{tile}{RESET}"
            elif tile in ["[", "]"]:
                row_output += f"{LIGHT_GREEN}{tile}{RESET}"
            elif tile == "@":
                row_output += f"{YELLOW}{tile}{RESET}"
            else:
                row_output += tile
        print(row_output)
    # time.sleep(0.1)


def compute_gps_coordinates(grid, target_symbol = "["):
    """
    Return the sum of GPS coordinates for all boxes with the target symbol.
    """
    positions = np.vstack(np.where(grid == target_symbol)).T
    return int(np.sum(positions[:, 0] * 100 + positions[:, 1]))

def process_horizontal_movement(warehouse, robot_pos, move):
    if move == "<":
        ahead = warehouse[robot_pos[0], robot_pos[1]::-1]
    else:
        ahead = warehouse[robot_pos[0], robot_pos[1]:]

    linepos, linelen = 0, 1
    for i in range(1, len(ahead)):
        if ahead[i] == ".":
            for j in range(linelen):
                ahead[i - j] = ahead[i - 1 - j]
            ahead[linepos] = "."
            break
        elif ahead[i] in ["[", "]"]:
            linelen += 1
        elif ahead[i] == "#":
            break


def process_vertical_movement(field, robot_pos, dir):
    """
    Handle vertical robot movement and manage connected boxes.

    Args:
        field (np.ndarray): The 2D array representing the warehouse grid.
        pos (np.ndarray): The current position of the robot.
        dir (np.ndarray): The movement direction as a 2D vector.

    Returns:
        None
    """
    next_pos = tuple(robot_pos + dir)
    if field[next_pos] == ".":
        field[next_pos] = "@"
        field[tuple(robot_pos)] = "."
    elif field[next_pos] in ["[", "]"]:
        cand = [robot_pos + dir]
        cluster = []
        while cand:
            check = cand.pop(0)
            if field[tuple(check)] == "]":
                cluster += [check, check + [0, -1]]
                cand += [check + [dir[0], 0], check + [dir[0], -1]]
            elif field[tuple(check)] == "[":
                cluster += [check, check + [0, 1]]
                cand += [check + [dir[0], 0], check + [dir[0], 1]]
        cluster = [np.array(item) for item in {tuple(arr) for arr in cluster}]
        blocked = any(field[tuple(element + dir)] == "#" for element in cluster)
        if not blocked:
            for element in sorted(cluster, key=lambda x: x[0], reverse=dir[0] + 1):
                field[tuple(element + dir)] = field[tuple(element)]
                field[tuple(element)] = "."
            field[next_pos] = "@"
            field[tuple(robot_pos)] = "."


def simulate_robot_movements(field, movements):
    """
    Simulate the robot's movements based on the movement sequence.

    Args:
        field (np.ndarray): The 2D array representing the warehouse grid.
        movements (str): The sequence of robot movements.

    Returns:
        None
    """
    for move in movements:
        pos = np.hstack((field == "@").nonzero())
        if move in ["<", ">"]:
            process_horizontal_movement(field, pos, move)
        elif move in ["^", "v"]:
            dir = np.array([-1, 0] if move == "^" else [1, 0])
            process_vertical_movement(field, pos, dir)
        # print_grid(field)  # Optional: Visualize grid after every move


if __name__ == "__main__":
    grid, movements = load_input("./day_15/day_15_input.txt")
    warehouse = double_width(grid)
    print_grid(warehouse) 

    simulate_robot_movements(warehouse, movements)
    result = compute_gps_coordinates(warehouse)

    print_grid(warehouse)  
    print(f"Sum of GPS coordinates: {result}")