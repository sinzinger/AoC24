"""
--- Part Two ---
While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

75,97,47,61,53 becomes 97,75,47,61,53.
61,13,29 becomes 61,29,13.
97,13,75,29,47 becomes 97,75,47,29,13.
After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?
"""

import networkx as nx
import time

start_time = time.time()

# Load data from file
with open("day_05_input.txt", "r") as f:
    lines = f.read().strip().split("\n")

# Parse the dependency rules and updates
rules = []
updates = []
is_parsing_updates = False

for line in lines:
    if not is_parsing_updates and "|" in line:
        # Parse dependency rules
        x, y = map(int, line.split("|"))
        rules.append((x, y))
    elif is_parsing_updates or "," in line:
        # Parse updates
        is_parsing_updates = True
        update = list(map(int, line.split(",")))
        updates.append(update)

# Build the directed graph from rules
graph = nx.DiGraph()
graph.add_edges_from(rules)

def is_valid_update(graph, update):
    """Check if the given update is a valid topological order in the graph."""
    positions = {page: i for i, page in enumerate(update)}
    for u, v in graph.edges():
        if u in positions and v in positions:
            if positions[u] > positions[v]:  # Rule violated
                return False
    return True

def correct_update(graph, update):
    """Reorder the update based on the topological sorting."""
    subgraph = graph.subgraph(update)  # Extract relevant subgraph
    return list(nx.topological_sort(subgraph))

# Validate updates and correct the invalid ones
invalid_updates = []
corrected_middle_pages = []

for update in updates:
    if not is_valid_update(graph, update):
        invalid_updates.append(update)
        corrected_update = correct_update(graph, update)
        corrected_middle_pages.append(corrected_update[len(corrected_update) // 2])

# Sum of middle pages from corrected updates
result = sum(corrected_middle_pages)

# Outputs
print("Invalid Updates:", invalid_updates)
print("Corrected Middle Pages:", corrected_middle_pages)
print("Sum of Corrected Middle Pages:", result)

end_time = time.time()  # End timer
print(f"Execution Time: {end_time - start_time:.4f} seconds")