import networkx as nx

def find_largest_clique(connections):
    # Step 1: Build the graph
    G = nx.Graph()
    for conn in connections:
        a, b = conn.split("-")
        G.add_edge(a, b)
    
    # Step 2: Find all maximal cliques
    cliques = list(nx.find_cliques(G))
    
    # Step 3: Identify the largest clique
    largest_clique = max(cliques, key=len)
    
    # Step 4: Generate the password
    password = ",".join(sorted(largest_clique))
    return password

def main():
    connections = open ("./day_23/day_23_input.txt", "r").read().split("\n")
    password = find_largest_clique(connections)
    print("Password to the LAN party:", password)

if __name__ == "__main__":
    main()