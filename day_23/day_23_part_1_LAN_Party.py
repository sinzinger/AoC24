from collections import defaultdict

def find_triangles_with_t(connections):
    # Step 1: Parse input into adjacency list
    graph = defaultdict(set)
    for conn in connections:
        a, b = conn.split("-")
        graph[a].add(b)
        graph[b].add(a)
    
    # Step 2: Identify relevant nodes (names starting with 't')
    relevant_nodes = {node for node in graph if node.startswith('t')}
    
    # Step 3: Find triangles involving relevant nodes
    triangles = set()
    for node in relevant_nodes:
        for neighbor in graph[node]:
            # Look for common neighbors
            common_neighbors = graph[node].intersection(graph[neighbor])
            for cn in common_neighbors:
                # Sort the triangle to avoid duplicates
                triangle = tuple(sorted([node, neighbor, cn]))
                triangles.add(triangle)
    
    # Step 4: Return results
    return len(triangles), triangles

def main():
    connections = open ("./day_23/day_23_input.txt", "r").read().split("\n")

    # Solve the problem
    count, triangles_with_t = find_triangles_with_t(connections)
    print("Number of triangles containing 't':", count)

if __name__ == "__main__":
    main()