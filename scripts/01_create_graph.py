import numpy as np

from route_optimization.graph import create_mining_graph
from route_optimization.visualization.graph import plot_graph

if __name__ == "__main__":
    np.random.seed(10)
    N = 4

    G_mine, dist_matrix, positions = create_mining_graph(N, n_blocks=2)

    print(f"Graph generated with {N} sites")
    print(f"Distance example (node 0 to node 1): {dist_matrix[0][1]:.2f}")
    print("\nDistance matrix:")
    print(dist_matrix)

    plot_graph(G_mine, positions)
