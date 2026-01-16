import dimod
import networkx as nx
import numpy as np

from route_optimization.graph import create_mining_graph
from route_optimization.model.qubo import create_hamiltonian
from route_optimization.visualization.graph import plot_graph


def create_graph(
    n: int,
    n_blocks: int,
) -> tuple[nx.Graph, np.ndarray, dict[int, np.ndarray]]:
    G_mine, dist_matrix, positions = create_mining_graph(n, n_blocks=n_blocks)

    print(f"Graph generated with {N} sites")
    print(f"Distance example (node 0 to node 1): {dist_matrix[0][1]:.2f}")
    print("\nDistance matrix:")
    print(dist_matrix)
    plot_graph(G_mine, positions)

    return G_mine, dist_matrix, positions


def create_hamilt(
    dist_matrix: np.ndarray,
    a_coef: float,
    b_coef: float,
) -> tuple[dimod.BinaryQuadraticModel, int, int]:
    bqm = create_hamiltonian(dist_matrix, a_coef, b_coef)

    num_qubits = len(bqm.variables)
    num_interactions = len(bqm.quadratic)

    print("\nModel generated successfully.")
    print(f"Variables (qubits): {num_qubits} (for N={len(dist_matrix)})")
    print(f"Coupling (interactions): {num_interactions}")

    return bqm, num_qubits, num_interactions


if __name__ == "__main__":
    np.random.seed(10)
    N = 4

    G_mine, dist_matrix, positions = create_graph(N, n_blocks=2)

    bqm, n_qubits, n_interactions = create_hamilt(dist_matrix, a_coef=0.0, b_coef=1.0)
