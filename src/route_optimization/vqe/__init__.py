from dimod import BinaryQuadraticModel
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import real_amplitudes
from qiskit.quantum_info import SparsePauliOp

from route_optimization.model.converter import bqm_to_qp, qp_to_ising


def prepare_problem(
    bqm: BinaryQuadraticModel,
) -> tuple[SparsePauliOp, QuantumCircuit, float]:
    qp = bqm_to_qp(bqm)
    hamiltonian, offset = qp_to_ising(qp)

    n_qubit = hamiltonian.num_qubits
    if n_qubit is None:
        raise Exception("Error: hamiltonian qubit count is NaN")

    ansatz = real_amplitudes(
        num_qubits=n_qubit,
        entanglement="linear",
        reps=1,
    )

    print(f"Ansatz parameters: {ansatz.num_parameters}")

    return hamiltonian, ansatz, offset
