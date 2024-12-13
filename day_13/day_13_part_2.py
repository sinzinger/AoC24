import numpy as np

def parse_input(file_path):
    machines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):  # Each machine has 3 lines of data
            a_line = lines[i].strip().split(", ")
            b_line = lines[i + 1].strip().split(", ")
            prize_line = lines[i + 2].strip().split(", ")
            
            # Extract values
            x_a, y_a = map(int, [a_line[0].split("+")[1], a_line[1].split("+")[1]])
            x_b, y_b = map(int, [b_line[0].split("+")[1], b_line[1].split("+")[1]])
            prize_x, prize_y = map(int, [prize_line[0].split("=")[1], prize_line[1].split("=")[1]])
            prize_x += 10**13
            prize_y += 10**13
            print(x_a, y_a, x_b, y_b, prize_x, prize_y)

            
            machines.append({
                "A": (x_a, y_a, 3),  # A button moves and costs 3 tokens
                "B": (x_b, y_b, 1),  # B button moves and costs 1 token
                "Prize": (prize_x, prize_y),
            })
    return machines

def solve_with_matrix(machines):
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
                if (presses_a * x_a + presses_b * x_b == prize_x and
                        presses_a * y_a + presses_b * y_b == prize_y):
                    # Calculate the total cost
                    tokens = presses_a * cost_a + presses_b * cost_b
                    total_tokens += tokens
                    prizes_won += 1
                    print(f"Machine {i+1}: Won the prize with {presses_a} A presses and {presses_b} B presses. Tokens spent: {tokens}")
                else:
                    print(f"Machine {i+1}: No valid solution. Prize cannot be won.")
            else:
                print(f"Machine {i+1}: No valid integer solution found. Prize cannot be won.")

        except np.linalg.LinAlgError:
            print(f"Machine {i+1}: Movement matrix is not invertible. Prize cannot be won.")

    # Output results
    print(f"\nTotal prizes won: {prizes_won}")
    print(f"Total tokens spent: {total_tokens}")

# Example input data
machines = [
    {"A": (94, 34, 3), "B": (22, 67, 1), "Prize": (10000000008400, 10000000005400)},
    {"A": (26, 66, 3), "B": (67, 21, 1), "Prize": (10000000012748, 10000000012176)},
    {"A": (17, 86, 3), "B": (84, 37, 1), "Prize": (10000000007870, 10000000006450)},
    {"A": (69, 23, 3), "B": (27, 71, 1), "Prize": (10000000018641, 10000000010279)},
]

input_file = "./day_13/day_13_input.txt"
machines = parse_input(input_file)

# Solve the problem
solve_with_matrix(machines)