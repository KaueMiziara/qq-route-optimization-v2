import numpy as np
from dimod import BinaryQuadraticModel
from qiskit.quantum_info.states.statevector import SparsePauliOp
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.converters import QuadraticProgramToQubo


def bqm_to_qp(bqm: BinaryQuadraticModel) -> QuadraticProgram:
    qp = QuadraticProgram(name="Mining Optimization")

    sorted_vars = sorted(list(bqm.variables), key=str)

    var_to_idx = {var: i for i, var in enumerate(sorted_vars)}
    n_vars = len(sorted_vars)

    for var in sorted_vars:
        qp.binary_var(name=str(var))

    linear_array = np.zeros(n_vars)
    for var, bias in bqm.linear.items():
        idx = var_to_idx[var]
        linear_array[idx] = bias

    quadratic_matrix = np.zeros((n_vars, n_vars))
    for (u, v), bias in bqm.quadratic.items():
        idx_u = var_to_idx[u]
        idx_v = var_to_idx[v]
        quadratic_matrix[idx_u, idx_v] = bias

    qp.minimize(
        constant=float(bqm.offset),
        linear=linear_array,
        quadratic=quadratic_matrix,
    )

    return qp


def qp_to_ising(qp: QuadraticProgram) -> tuple[SparsePauliOp, float]:
    converter = QuadraticProgramToQubo()
    qubo = converter.convert(qp)
    return qubo.to_ising()
