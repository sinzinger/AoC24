"""
--- Part Two ---
The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
192: 17 8 14 can be made true using 17 || 8 + 14.
Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?
"""

import itertools
import time
from concurrent.futures import ProcessPoolExecutor

def parse_input(file_path):
    """Parse the input file into target values and number sequences."""
    equations = []
    with open(file_path, "r") as f:
        for line in f:
            target, numbers = line.strip().split(":")
            target = int(target)
            numbers = list(map(int, numbers.split()))
            equations.append((target, numbers))
    return equations

def is_equation_solvable(target, numbers):
    """Check if any operator combination makes the equation true."""
    operators = ["+", "*", "||"]

    # Generate and evaluate combinations directly
    operator_combinations = itertools.product(operators, repeat=len(numbers) - 1)
    for combination in operator_combinations:
        result = numbers[0]
        for i, operator in enumerate(combination):
            if operator == "+":
                result += numbers[i + 1]
            elif operator == "*":
                result *= numbers[i + 1]
            elif operator == "||":
                result = int(str(result) + str(numbers[i + 1]))

            # Prune combinations that exceed the target
            # Interesting: now with parallel processing pruning is efficient. From 1.3 to 1.2 seconds 🚀
            if result > target:
                break

        if result == target:
            return True

    return False

def calculate_single_equation(equation):
    """Evaluate whether a single equation can be solved."""
    target, numbers = equation
    return target if is_equation_solvable(target, numbers) else 0   

def calculate_total_calibration(equations):

    """Calculate the total calibration result using parallel processing."""
    # This decreased execution time from 8.6 to 1.3 seconds. 🚀
    with ProcessPoolExecutor() as executor:
        results = executor.map(calculate_single_equation, equations)
    return sum(results)

if __name__ == "__main__":
    # Start timing
    start_time = time.time()

    # Parse input
    file_path = "day_07_input.txt"  # Replace with your actual input file path
    equations = parse_input(file_path)

    # Calculate total calibration result
    total_calibration = calculate_total_calibration(equations)

    # Output the result
    print("Total Calibration Result:", total_calibration)

    # End timing
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
