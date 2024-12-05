import networkx as nx
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
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

# Precompute dependency subgraphs for updates
@lru_cache(maxsize=None)  # Cache results for efficiency
def get_subgraph_nodes(update):
    return set(update) & set(graph.nodes)

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
    subgraph_nodes = get_subgraph_nodes(tuple(update))
    subgraph = graph.subgraph(subgraph_nodes)  # Extract relevant subgraph
    return list(nx.topological_sort(subgraph))

# Process updates in parallel
def process_update(update):
    """Validate and correct a single update."""
    if not is_valid_update(graph, update):
        corrected_update = correct_update(graph, update)
        middle_page = corrected_update[len(corrected_update) // 2]
        return middle_page
    return None

# Use ThreadPoolExecutor for parallel processing
corrected_middle_pages = []
with ThreadPoolExecutor() as executor:
    results = executor.map(process_update, updates)
    corrected_middle_pages = [res for res in results if res is not None]

# Sum of middle pages from corrected updates
result = sum(corrected_middle_pages)

# Outputs
print("Sum of Corrected Middle Pages:", result)
end_time = time.time()  # End timer
print(f"Execution Time: {end_time - start_time:.4f} seconds")