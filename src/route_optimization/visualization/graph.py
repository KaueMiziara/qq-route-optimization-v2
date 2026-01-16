import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from route_optimization.visualization import open_image_external, save_plot


def plot_graph(graph: nx.Graph, pos: dict[int, np.ndarray]) -> None:
    plt.figure(figsize=(6, 6))
    nx.draw(graph, pos, with_labels=True, node_color="orange", node_size=800)
    plt.title("Miner map")

    saved_path = save_plot("initial_graph")
    print(f"\nSaved graph: {saved_path}")

    plt.close()

    open_image_external(saved_path)
