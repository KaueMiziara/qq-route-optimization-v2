import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

from route_optimization.visualization import open_image_external, save_plot


def plot_graph(graph: nx.Graph, pos: dict[int, np.ndarray]) -> None:
    plt.figure(figsize=(6, 6))
    nx.draw(graph, pos, with_labels=True, node_color="orange", node_size=800)
    plt.title("Miner map")

    saved_path = save_plot("initial_graph")
    print(f"\nSaved graph: {saved_path}")

    plt.close()

    open_image_external(saved_path)


def plot_digraph(
    graph: nx.Graph,
    pos: dict[int, np.ndarray],
    route: np.ndarray,
) -> None:
    plt.figure(figsize=(10, 8))

    nx.draw_networkx_nodes(graph, pos, node_color="#e0e0e0", node_size=600, alpha=0.8)
    nx.draw_networkx_edges(graph, pos, edge_color="#d3d3d3", style="dashed", alpha=0.4)
    nx.draw_networkx_labels(graph, pos, font_family="sans-serif", font_weight="bold")

    if -1 in route:
        print("\nThe route contains invalid nodes (-1)! Impossible to plot path.")
        return

    route_edges = []
    num_steps = len(route)
    start_node = route[0]

    print(f"Node sequence: {route} -> {start_node} (Cyclic)")

    for i in range(num_steps):
        origin = route[i]
        target = route[(i + 1) % num_steps]
        route_edges.append((origin, target))

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=route_edges,
        edge_color="#D9534F",
        width=3.0,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=25,
        connectionstyle="arc3,rad=0.1",
    )

    for i, (u, v) in enumerate(route_edges):
        x_m = (pos[u][0] + pos[v][0]) / 2
        y_m = (pos[u][1] + pos[v][1]) / 2

        plt.text(
            x_m,
            y_m,
            f"{i + 1}",
            fontsize=10,
            color="white",
            fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.3", fc="#D9534F", ec="none", alpha=0.8),
        )

    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=[start_node],
        node_color="#5CB85C",
        node_size=800,
        label="Start/End",
    )

    plt.title("Optimal Fleet Route", fontsize=14)
    plt.axis("off")

    elements_subtitles = [
        Line2D([0], [0], color="#D9534F", lw=3, label="Ruta Óptima (VQE)"),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#5CB85C",
            markersize=12,
            label="Punto de Inicio",
        ),
        Line2D([0], [0], color="#d3d3d3", lw=1, linestyle="--", label="Possible Paths"),
    ]

    plt.legend(handles=elements_subtitles, loc="lower right")

    saved_path = save_plot("final_graph")
    print(f"\nSaved graph: {saved_path}")

    plt.close()

    open_image_external(saved_path)
