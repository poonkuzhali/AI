import math
from queue import PriorityQueue

import networkx as nx
from matplotlib import pyplot as plt


def a_star_implementation(graph, pos, start, target, obstacles):
    # Heuristics
    for node in graph.nodes():
        h = round(math.dist(pos[node], pos[target]), 2)
        graph.nodes[node]["h"] = h
    hold_q = PriorityQueue()  # Priority queue which acts as the open list for A star.
    closed = []  # Closed list to add nodes which are explored.
    hold_q.put((0, start))
    graph.nodes[start]["distance"] = 0
    path = {start: None}  # Path dictionary will have the key and value as node and its parent respectively.
    while hold_q.qsize() != 0:
        node_to_explore = hold_q.get()
        node_to_explore = node_to_explore[1]
        closed.append(node_to_explore)

        if node_to_explore == target:
            break
        neighbors = [n for n in graph.neighbors(node_to_explore)]  # Connected nodes
        for node in neighbors:
            if node not in obstacles and node not in closed:
                g = graph.nodes[node_to_explore]["distance"] + graph.edges[(node_to_explore, node)]["weight"]
                if graph.nodes[node].get("distance", 0) == 0 or g < graph.nodes[node].get("distance", 0):
                    graph.nodes[node]["distance"] = g
                    f = round(g + graph.nodes[node]["h"], 2)
                    hold_q.put((f, node))
                    path[node] = node_to_explore if node != start else None

            else:
                closed.append(node)

    inbuilt_methods(graph, start, target, pos)  # For verification purposes

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
        plt.show()
        print("-----------------------------------------------------------------------------------"
              "-------------------------")

        print("View images saved in the same folder for the in-built dijkstra(dijkstra.png), "
              "in-built a-star(inbuilt_astar.png) and implemented a-star(astar.png)")

        print("---------------------------------------------------------------------------------------"
              "---------------------")


def inbuilt_methods(graph, start, target, pos):
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
    print(
        "------------------------------------------------------------------------------------------------------------")
