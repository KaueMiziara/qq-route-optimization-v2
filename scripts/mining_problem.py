import dimod
import networkx as nx
import numpy as np
from qiskit import QuantumCircuit
from qiskit_optimization import QuadraticProgram
from scipy.optimize import OptimizeResult

from route_optimization.graph import create_mining_graph
from route_optimization.logger import Logger
from route_optimization.model.qubo import create_hamiltonian
from route_optimization.solution import interpret_solution
from route_optimization.visualization.convergence import plot_convergence
from route_optimization.visualization.graph import plot_digraph, plot_graph
from route_optimization.vqe import run_vqe


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


def create_problem(
    dist_matrix: np.ndarray,
    a_coef: float,
    b_coef: float,
) -> dimod.BinaryQuadraticModel:
    bqm = create_hamiltonian(dist_matrix, a_coef, b_coef)

    num_qubits = len(bqm.variables)
    num_interactions = len(bqm.quadratic)

    print("\nModel generated successfully.")
    print(f"Variables (qubits): {num_qubits} (for N={len(dist_matrix)})")
    print(f"Coupling (interactions): {num_interactions}")

    return bqm


def execute_vqe(
    bqm: dimod.BinaryQuadraticModel,
) -> tuple[OptimizeResult, QuantumCircuit, float, QuadraticProgram, Logger]:
    opt_result, opt_ansatz, final_energy, qp, log = run_vqe(bqm, Logger())
    print(f"\nMinimum energy reached: {final_energy:.4f}")

    return opt_result, opt_ansatz, final_energy, qp, log


def get_results(
    ansatz: QuantumCircuit,
    params: np.ndarray,
    qp: QuadraticProgram,
) -> np.ndarray:
    print("\n--- Interpreting Results ---")

    final_route = interpret_solution(ansatz, params, qp)
    print("\nOptimal route:", final_route)

    return np.array(final_route)


if __name__ == "__main__":
    np.random.seed(10)
    N = 4

    G_mine, dist_matrix, positions = create_graph(N, n_blocks=2)

    bqm = create_problem(dist_matrix, a_coef=0.0, b_coef=1.0)

    opt_result, opt_ansatz, final_energy, qp, log = execute_vqe(bqm)

    plot_convergence(log)

    final_route = get_results(opt_ansatz, opt_result.x, qp)

    plot_digraph(G_mine, positions, final_route)
