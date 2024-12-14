import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Grid dimensions
WIDTH = 101
HEIGHT = 103

def parse_input_file(filename):
    """
    Reads the input file and parses the positions and velocities of robots.
    Each line in the file has the format: p=x,y v=dx,dy
    """
    robots = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            pos = parts[0].split("=")[1]
            vel = parts[1].split("=")[1]
            px, py = map(int, pos.split(","))
            vx, vy = map(int, vel.split(","))
            robots.append({"px": px, "py": py, "vx": vx, "vy": vy})
    return robots

def generate_grid(robots, width, height):
    """
    Generate a grid visualization with robot positions.
    """
    grid = [[0 for _ in range(width)] for _ in range(height)]
    for robot in robots:
        grid[robot["py"]][robot["px"]] = 1  # Mark robot positions
    return grid

def save_grid_as_image(grid, iteration, folder="grids"):
    """
    Save the grid as an image using Matplotlib with light green robots.
    """
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Create a custom colormap
    cmap = mcolors.ListedColormap(["black", "lightgreen"])
    bounds = [0, 0.5, 1]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # Create the image
    plt.figure(figsize=(WIDTH / 10, HEIGHT / 10), dpi=100)
    plt.imshow(grid, cmap=cmap, norm=norm, interpolation="nearest")
    plt.axis("off")  # Hide axes

    # Save the image
    filename = os.path.join(folder, f"grid_{iteration:05d}.png")
    plt.savefig(filename, bbox_inches="tight", pad_inches=0)
    plt.close()

def simulate_and_save(robots, width, height, max_iterations=10000, save_folder="grids"):
    """
    Simulate robot movements and save each grid as an image.
    """
    for iteration in range(max_iterations):
        for robot in robots:
            robot["px"] = (robot["px"] + robot["vx"]) % width
            robot["py"] = (robot["py"] + robot["vy"]) % height

        grid = generate_grid(robots, width, height)
        save_grid_as_image(grid, iteration, folder=save_folder)
        print(f"Iteration {iteration + 1} saved.")

# Main function
if __name__ == "__main__":
    input_file = "./day_14/day_14_input.txt"
    robots = parse_input_file(input_file)
    simulate_and_save(robots, WIDTH, HEIGHT)