"""
--- Day 13: Claw Contraption ---
Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.
The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
"""

from pulp import LpProblem, LpVariable, LpMinimize, value



# Define claw machine configurations
# machines = [
#     {"A": (94, 34, 3), "B": (22, 67, 1), "Prize": (8400, 5400)},
#     {"A": (26, 66, 3), "B": (67, 21, 1), "Prize": (12748, 12176)},
#     {"A": (17, 86, 3), "B": (84, 37, 1), "Prize": (7870, 6450)},
#     {"A": (69, 23, 3), "B": (27, 71, 1), "Prize": (18641, 10279)},
    # ]

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
            
            machines.append({
                "A": (x_a, y_a, 3),  # A button moves and costs 3 tokens
                "B": (x_b, y_b, 1),  # B button moves and costs 1 token
                "Prize": (prize_x, prize_y),
            })
    return machines

input_file = "./day_13/day_13_input.txt"
machines = parse_input(input_file)

# Define the maximum button presses
max_presses = 100

# Results storage
total_tokens = 0
prizes_won = 0

for i, machine in enumerate(machines):
    x_a, y_a, cost_a = machine["A"]
    x_b, y_b, cost_b = machine["B"]
    prize_x, prize_y = machine["Prize"]

    # Define the optimization problem
    prob = LpProblem(f"Machine_{i+1}", LpMinimize)

    # Variables: number of presses for A and B
    presses_a = LpVariable("Presses_A", lowBound=0, upBound=max_presses, cat="Integer")
    presses_b = LpVariable("Presses_B", lowBound=0, upBound=max_presses, cat="Integer")

    # Objective: Minimize the cost (tokens spent)
    prob += presses_a * cost_a + presses_b * cost_b, "Total_Cost"

    # Constraints: Achieve the exact position of the prize
    prob += presses_a * x_a + presses_b * x_b == prize_x, "X_Position"
    prob += presses_a * y_a + presses_b * y_b == prize_y, "Y_Position"

    # Solve the problem
    status = prob.solve()

    # Check if the problem has a feasible solution
    if status == 1:  # Solution found
        tokens = value(presses_a * cost_a + presses_b * cost_b)
        total_tokens += tokens
        prizes_won += 1
        print(f"Machine {i+1}: Won the prize with {value(presses_a)} A presses and {value(presses_b)} B presses. Tokens spent: {tokens}")
    else:
        print(f"Machine {i+1}: No solution found. Prize cannot be won.")

# Output results
print(f"\nTotal prizes won: {prizes_won}")
print(f"Total tokens spent: {total_tokens}")