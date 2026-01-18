from typing import Any, cast

import numpy as np
from dimod import BinaryQuadraticModel
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import real_amplitudes
from qiskit.primitives import StatevectorEstimator
from qiskit.primitives.containers.estimator_pub import EstimatorPub
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import OptimizeResult, minimize

from route_optimization.logger import Logger
from route_optimization.model.converter import bqm_to_qp, qp_to_ising


def _prepare_problem(
    bqm: BinaryQuadraticModel,
) -> tuple[SparsePauliOp, QuantumCircuit, float]:
    qp = bqm_to_qp(bqm)
    hamiltonian, offset = qp_to_ising(qp)

    n_qubit = hamiltonian.num_qubits
    if n_qubit is None:
        raise ValueError("Error: hamiltonian qubit count is NaN")

    ansatz = real_amplitudes(
        num_qubits=n_qubit,
        entanglement="linear",
        reps=1,
    )

    return hamiltonian, ansatz, offset


def run_vqe(
    bqm: BinaryQuadraticModel,
    log: Logger,
) -> tuple[OptimizeResult, QuantumCircuit, float, Logger]:
    hamilt, ansatz, offset = _prepare_problem(bqm)
    estimator = StatevectorEstimator()

    num_parameters = ansatz.num_parameters
    init_params = 2 * np.pi * np.random.rand(num_parameters)

    print(f"Ansatz parameters: {ansatz.num_parameters}")
    print(f"Initial parameter list: {init_params}")

    def cost_func_wrapper(params) -> float:
        params_flat = np.array(params).flatten()

        if len(params_flat) != ansatz.num_parameters:
            raise ValueError(
                f"Error: Ansatz requires {ansatz.num_parameters} parameters, "
                f"received {len(params_flat)}"
            )

        param_dict = dict(zip(ansatz.parameters, params_flat, strict=True))

        pub = EstimatorPub.coerce((ansatz, [hamilt], param_dict))
        job = estimator.run([pub])
        result = job.result()

        pub_result_data = cast(Any, result[0].data)
        energy = float(pub_result_data.evs[0])

        log.register_energy(energy)
        return energy

    print("\nStarting VQE")

    res = minimize(
        cost_func_wrapper,
        init_params,
        method="COBYLA",
        options={"maxiter": 500, "disp": True},
    )

    final_energy = float(res.fun) + offset

    return res, ansatz, final_energy, log
