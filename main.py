import math

import networkx as nx
from matplotlib import pyplot as plt
from queue import PriorityQueue


def create_graph():
    graph = nx.read_adjlist("graph.txt", nodetype=int)
    print(f"Graph has {graph.number_of_nodes()} nodes!")
    start = int(input("Enter start node: "))
    target = int(input("Enter target node: "))
    obstacles = []
    obstacle = int(input("Enter obstacle node: "))
    while obstacle != 0:
        obstacles.append(obstacle)
        obstacle = int(input("Enter obstacle node: "))
    print("------------------------------------------------------------------------------------------------------------")
    pos = {}
    with open("coords.txt", "r") as file:
        for line in file:
            coords = line.split()
            node_id = int(coords[0])
            x = float(coords[1])
            y = float(coords[2])
            pos[node_id] = (x, y)
    for edge in graph.edges():
        node1 = int(edge[0])
        node2 = int(edge[1])
        weight = round(math.dist(pos[node1], pos[node2]), 2)
        # print(f"{edge} {weight}")
        graph.add_edge(node1, node2, weight=weight)
    # plt.gca().invert_yaxis()
    # nx.draw(graph, pos=pos, with_labels=True, node_size=500)
    #
    # plt.show()
    a_star_implementation(graph, pos, start, target, obstacles)


def a_star_implementation(graph, pos, start, target, obstacles):
    for node in graph.nodes():
        h = round(math.dist(pos[node], pos[target]), 2)
        graph.nodes[node]["h"] = h
        # print(graph.nodes[node])
    holdq = PriorityQueue()
    closed = []
    holdq.put((0, start))
    graph.nodes[start]["distance"] = 0
    path = {start: None}
    while holdq.qsize() != 0:
        node_to_explore = holdq.get()
        node_to_explore = node_to_explore[1]
        closed.append(node_to_explore)

        if node_to_explore == target:
            break
        neighbors = [n for n in graph.neighbors(node_to_explore)]
        for node in neighbors:
            if node not in obstacles and node not in closed:
                g = graph.nodes[node_to_explore]["distance"] + graph.edges[(node_to_explore, node)]["weight"]
                if graph.nodes[node].get("distance", 0) == 0 or g < graph.nodes[node].get("distance", 0):
                    # print(f"g cost for {node} is {g}")
                    graph.nodes[node]["distance"] = g
                    f = round(g + graph.nodes[node]["h"], 2)
                    holdq.put((f, node))
                    path[node] = node_to_explore if node != start else None

            else:
                closed.append(node)

    print("Note: Obstacles haven't been used for the built-in functions")
    dijkstra_path = nx.dijkstra_path(graph, start, target, weight="weight")
    print(f"Path generated using built-in dijkstra: {dijkstra_path}")
    plt.gca().invert_yaxis()
    node_colors = ["green" if n in dijkstra_path else "blue" for n in graph.nodes()]
    nx.draw(graph, pos=pos, with_labels=True, node_size=500, node_color=node_colors)
    plt.savefig("dijkstra.png")

    def heuristic(node1, node2):
        return graph.nodes[node1]['h']

    a_star = nx.astar_path(graph, start, target, heuristic=heuristic, weight="weight")
    print(f"Path generated using built-in A star {a_star}")
    node_colors = ["green" if n in a_star else "blue" for n in graph.nodes()]
    nx.draw(graph, pos=pos, with_labels=True, node_size=500, node_color=node_colors)
    plt.savefig("inbuilt_astar.png")
    print("------------------------------------------------------------------------------------------------------------")

    astar_path = []
    if path.get(target) is None:
        print("No path found using A star!")
    else:
        while path[target] is not None:
            astar_path.append(target)
            target = path[target]
        astar_path.append(start)
        astar_path.reverse()
        print(f"Path found using my A star implementation: {astar_path}")
        node_colors = []
        for n in graph.nodes():
            if n in astar_path:
                node_colors.append("green")
            elif n in obstacles:
                node_colors.append("red")
            else:
                node_colors.append("blue")
        nx.draw(graph, pos=pos, with_labels=True, node_size=500, node_color=node_colors)

        plt.savefig("astar.png")


if __name__ == "__main__":
    create_graph()
