import numpy as np
from dimod import BINARY, BinaryQuadraticModel


def create_hamiltonian(
    dist_matrix: np.ndarray,
    a_coef: float = 0.0,
    b_coef: float = 1.0,
) -> BinaryQuadraticModel:
    N = len(dist_matrix)
    max_dist = np.max(dist_matrix)

    if a_coef == 0.0:
        a_coef = b_coef * max_dist * 2.0
        print(
            f"Constant A calculated automatically: {a_coef:.2f} (Max dist: {max_dist})"
        )

    bqm = BinaryQuadraticModel(BINARY)

    for i in range(N):
        for t in range(N):
            var_name = __get_var(i, t)
            bqm.add_variable(var_name, -2 * a_coef)

    for t in range(N):
        for i in range(N):
            for j in range(i + 1, N):
                u = __get_var(i, t)
                v = __get_var(j, t)
                bqm.add_interaction(u, v, 2 * a_coef)

    for i in range(N):
        for t in range(N):
            for k in range(t + 1, N):
                u = __get_var(i, t)
                v = __get_var(i, k)
                bqm.add_interaction(u, v, 2 * a_coef)

    for t in range(N):
        next_t = (t + 1) % N

        for i in range(N):
            for j in range(N):
                if i != j:
                    dist = dist_matrix[i][j]

                    u = __get_var(i, t)
                    v = __get_var(j, next_t)

                    bqm.add_interaction(u, v, b_coef * dist)

    return bqm


def __get_var(i: int, j: int) -> str:
    return f"x_{i}_{j}"
