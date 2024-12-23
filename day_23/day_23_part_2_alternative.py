import networkx as nx
connections = open ("./day_23/day_23_input.txt", "r").read().split("\n")
G = nx.Graph([conn.split("-") for conn in connections])
password = ",".join(sorted(max(nx.find_cliques(G), key=len)))
print("Password to the LAN party:", password)