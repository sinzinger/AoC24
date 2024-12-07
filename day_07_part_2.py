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
from functools import lru_cache

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

def evaluate_expression(numbers, operators):
    """Evaluate the expression left-to-right with the given operators."""
    #Interesting: Memoized evaluation of the expression resulted in an increase of the execution time from 8 to 20 seconds. 🧐
    #Interesting: Memoizing only the concatenation operation resulted in an increaes from 8.6 to 8.7 seconds 🧐
    result = numbers[0]  # Start with the first number
    for i in range(len(operators)):
        if operators[i] == "+":
            result += numbers[i + 1]  # Add the next number
        elif operators[i] == "*":
            result *= numbers[i + 1]  # Multiply with the next number
        elif operators[i] == "||":
            # Concatenate the next number as a string, then convert back to int
            result = int(str(result) + str(numbers[i + 1]))

        # Interesting: pruning resulted in an increase in execution time, 
        # it was better when applied before expensive multiplication operation
        # but still no pruning is more efficient. 🧐
        # Prune if result exceeds target before expensive multiplication operation
        #    if result > target:
        #        return False  # No need to evaluate further

    return result


def is_equation_solvable(target, numbers):
    """Check if any operator combination makes the equation true."""
    # Define operators as a list to treat "||" as a single operator
    operators = ["+", "*", "||"]

    # Generate all possible combinations of these operators
    operator_combinations = itertools.product(operators, repeat=len(numbers) - 1)

    for operators in operator_combinations:
        if evaluate_expression(numbers, operators) == target:
            return True
    return False


def calculate_total_calibration(equations):
    """Calculate the total calibration result."""
    total = 0
    for target, numbers in equations:
        if is_equation_solvable(target, numbers):
            total += target
    return total


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


"""
3. Parallelization
	•	Use concurrent.futures to evaluate different operator combinations concurrently.

4. Reduce Operator Combinations
	•	Remove operator combinations early that are unlikely to lead to the target value.
	•	Example: If concatenation (||) leads to a very large number compared to the target, skip it.

5. Precompute Concatenations
	•	Precompute all possible results of concatenation for the sequence of numbers. Use this to reduce the dynamic calculation of ||.
"""