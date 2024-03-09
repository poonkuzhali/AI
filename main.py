import math

import networkx as nx

from astar import a_star_implementation


def main():
    graph = nx.read_adjlist("graph.txt", nodetype=int)
    print(f"Graph has {graph.number_of_nodes()} nodes!")
    start = int(input("Enter start node: "))
    target = int(input("Enter target node: "))

    if start not in graph.nodes() or target not in graph.nodes():
        print("Invalid start and target nodes")
        exit()

    obstacles = []
    obstacle = input("Enter obstacle node, enter x to stop: ")
    try:
        while int(obstacle) >= 0:
            obstacles.append(int(obstacle))
            obstacle = int(input("Enter obstacle node, enter x to stop: "))
    except Exception as ex:
        print("End of receiving obstacles")
    print(
        "------------------------------------------------------------------------------------------------------------")
    pos = {}
    with open("coords.txt", "r") as file:
        for line in file:
            coords = line.split()
            node_id = int(coords[0])
            x = float(coords[1])
            y = float(coords[2])
            pos[node_id] = (x, y)

    # Calculating edge weights
    for edge in graph.edges():
        node1 = int(edge[0])
        node2 = int(edge[1])
        weight = round(math.dist(pos[node1], pos[node2]), 2)
        graph.add_edge(node1, node2, weight=weight)

    print(f'Obstacles {obstacles}')

    a_star_implementation(graph, pos, start, target, obstacles)


if __name__ == "__main__":
    main()
