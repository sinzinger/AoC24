"""
--- Day 14: Restroom Redoubt ---
One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near an unvisited location on their list, and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.

Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The area outside the bathroom is swarming with robots!

To get The Historian safely to the bathroom, you'll need a way to predict where the robots will be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight lines.

You make a list (your puzzle input) of all of the robots' current positions (p) and velocities (v), one robot per line. For example:

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
Each robot's position is given as p=x,y where x represents the number of tiles the robot is from the left wall and y represents the number of tiles from the top wall (when viewed from above). So, a position of p=0,0 means the robot is all the way in the top-left corner.

Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the robot is moving to the right, and positive y means the robot is moving down. So, a velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.

The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above). However, in this example, the robots are in a space which is only 11 tiles wide and 7 tiles tall.

The robots are good at navigating over/under each other (due to a combination of springs, extendable legs, and quadcopters), so they can share the same tile and don't interact with each other. Visually, the number of robots on each tile in this example looks like this:

1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...
These robots have a unique feature for maximum bathroom security: they can teleport. When a robot would run into an edge of the space they're in, they instead teleport to the other side, effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few seconds:

Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........
The Historian can't wait much longer, so you don't have to simulate the robots for very long. Where will the robots be after 100 seconds?

In the above example, the number of robots on each tile after 100 seconds has elapsed looks like this:

......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....
To determine the safest area, count the number of robots in each quadrant after 100 seconds. Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant, so the only relevant robots are:

..... 2..1.
..... .....
1.... .....
           
..... .....
...12 .....
.1... 1....
In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a total safety factor of 12.

Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?
"""

# Grid dimensions
WIDTH = 101
HEIGHT = 103
MIDDLE_COLUMN = WIDTH // 2  # Middle column (0-indexed)
MIDDLE_ROW = HEIGHT // 2    # Middle row (0-indexed)

# Time step
T = 100

def parse_input_file(filename):
    """
    Reads the input file and parses the positions and velocities of robots.
    Each line in the file has the format: p=x,y v=dx,dy
    """
    robots = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            parts = line.split()
            pos = parts[0].split("=")[1]  # Extract position
            vel = parts[1].split("=")[1]  # Extract velocity
            px, py = map(int, pos.split(","))
            vx, vy = map(int, vel.split(","))
            robots.append({"px": px, "py": py, "vx": vx, "vy": vy})
    return robots

def calculate_safety_factor(robots, width, height, time_step):
    middle_column = width // 2
    middle_row = height // 2

    # Initialize quadrant counters
    quadrant_counts = [0, 0, 0, 0]  # Q1, Q2, Q3, Q4

    # Process each robot
    for robot in robots:
        # Compute final position using modular arithmetic
        px_final = (robot["px"] + time_step * robot["vx"]) % width
        py_final = (robot["py"] + time_step * robot["vy"]) % height

        print ("px_final:", px_final, "py_final:", py_final)

        # Ignore robots in the middle row or middle column
        if px_final == middle_column or py_final == middle_row:
            continue

        # Determine quadrant
        if px_final < middle_column and py_final < middle_row:
            quadrant_counts[0] += 1  # Quadrant 1
        elif px_final > middle_column and py_final < middle_row:
            quadrant_counts[1] += 1  # Quadrant 2
        elif px_final < middle_column and py_final > middle_row:
            quadrant_counts[2] += 1  # Quadrant 3
        elif px_final > middle_column and py_final > middle_row:
            quadrant_counts[3] += 1  # Quadrant 4

    # Compute safety factor
    safety_factor = 1
    for count in quadrant_counts:
        safety_factor *= count

    return quadrant_counts, safety_factor

def main ():
    input_file = "./day_14/day_14_input.txt"
    robots = parse_input_file(input_file)
    quadrant_counts, safety_factor = calculate_safety_factor(robots, WIDTH, HEIGHT, T)
    print("Final Quadrant Counts:", quadrant_counts)
    print("Safety Factor:", safety_factor)

if __name__ == '__main__':
    main ()