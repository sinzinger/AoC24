"""
--- Part Two ---
As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
"""

import numpy as np
import logging
from typing import List, Dict, Tuple

# Constants
PRIZE_OFFSET = 10**13
COST_A = 3
COST_B = 1

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def parse_input(file_path: str) -> List[Dict[str, Tuple[int, int, int]]]:
    """
    Parses the input file to extract machine configurations.
    
    Args:
        file_path (str): Path to the input file.

    Returns:
        List[Dict[str, Tuple[int, int, int]]]: A list of machine configurations.
    """
    machines = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):  # Each machine has 3 lines of data
                a_line = lines[i].strip().split(", ")
                b_line = lines[i + 1].strip().split(", ")
                prize_line = lines[i + 2].strip().split(", ")

                # Extract values
                x_a, y_a = map(int, [a_line[0].split("+")[1], a_line[1].split("+")[1]])
                x_b, y_b = map(int, [b_line[0].split("+")[1], b_line[1].split("+")[1]])
                prize_x, prize_y = map(
                    int, [prize_line[0].split("=")[1], prize_line[1].split("=")[1]]
                )
                prize_x += PRIZE_OFFSET
                prize_y += PRIZE_OFFSET

                machines.append(
                    {
                        "A": (x_a, y_a, COST_A),  # A button moves and costs COST_A tokens
                        "B": (x_b, y_b, COST_B),  # B button moves and costs COST_B tokens
                        "Prize": (prize_x, prize_y),
                    }
                )
        return machines
    except FileNotFoundError:
        logger.error("Input file not found.")
        raise
    except Exception as e:
        logger.error(f"Error parsing input file: {e}")
        raise


def solve_with_matrix(machines: List[Dict[str, Tuple[int, int, int]]]) -> None:
    """
    Solves the problem using matrix algebra for each machine.

    Args:
        machines (List[Dict[str, Tuple[int, int, int]]]): A list of machine configurations.
    """
    total_tokens = 0
    prizes_won = 0

    for i, machine in enumerate(machines):
        x_a, y_a, cost_a = machine["A"]
        x_b, y_b, cost_b = machine["B"]
        prize_x, prize_y = machine["Prize"]

        # Construct the movement matrix and prize position vector
        M = np.array([[x_a, x_b], [y_a, y_b]])
        P = np.array([prize_x, prize_y])

        try:
            # Compute the inverse of the movement matrix
            M_inv = np.linalg.inv(M)

            # Solve for the number of button presses
            presses = np.dot(M_inv, P)

            # Check if the solution is valid (close to integer values)
            if np.all(np.isclose(presses, np.round(presses))):
                presses = np.round(presses).astype(int)
                presses_a, presses_b = presses

                # Verify the solution explicitly
                if (
                    presses_a * x_a + presses_b * x_b == prize_x
                    and presses_a * y_a + presses_b * y_b == prize_y
                ):
                    # Calculate the total cost
                    tokens = presses_a * cost_a + presses_b * cost_b
                    total_tokens += tokens
                    prizes_won += 1
                    logger.info(
                        f"Machine {i+1}: Won the prize with {presses_a} A presses and {presses_b} B presses. Tokens spent: {tokens}"
                    )
                else:
                    logger.info(f"Machine {i+1}: No valid solution. Prize cannot be won.")
            else:
                logger.info(
                    f"Machine {i+1}: No valid integer solution found. Prize cannot be won."
                )

        except np.linalg.LinAlgError:
            logger.info(f"Machine {i+1}: Movement matrix is not invertible. Prize cannot be won.")

    # Output results
    logger.info("\nSummary:")
    logger.info(f"Total prizes won: {prizes_won}")
    logger.info(f"Total tokens spent: {total_tokens}")


if __name__ == "__main__":
    INPUT_FILE = "./day_13/day_13_input.txt"

    try:
        machines = parse_input(INPUT_FILE)
        solve_with_matrix(machines)
    except Exception as e:
        logger.error(f"An error occurred: {e}")