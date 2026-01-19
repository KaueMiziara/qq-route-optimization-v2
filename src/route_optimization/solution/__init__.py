from collections.abc import Iterable
from typing import Any, cast

from numpy import ndarray
from qiskit.circuit import QuantumCircuit
from qiskit.primitives import SamplerPubLike, StatevectorSampler
from qiskit.primitives.containers.sampler_pub import SamplerPub
from qiskit_optimization import QuadraticProgram

from route_optimization.graph import decode_route


def interpret_solution(
    ansatz: QuantumCircuit,
    opt_params: ndarray,
    qp: QuadraticProgram,
) -> tuple[list[int], int]:
    sampler = StatevectorSampler()

    measurement_circuit = ansatz.copy()
    measurement_circuit.measure_all()

    opt_params_flat = opt_params.flatten()
    param_dict = dict(zip(measurement_circuit.parameters, opt_params_flat, strict=True))

    pub = SamplerPub.coerce((measurement_circuit, param_dict))
    pubs = cast(Iterable[SamplerPubLike], [pub])

    meas_job = sampler.run(pubs)
    result = meas_job.result()

    pub_result_data = cast(Any, result[0].data)
    counts = pub_result_data.meas.get_counts()

    best_bitstring: str = max(counts, key=counts.get)

    total_counts = sum(counts.values())
    probability = (counts[best_bitstring] / total_counts) * 100

    print(f"Most probable state: {best_bitstring} (Prob: {probability:.2f}%)")

    var_map = {v.name: i for i, v in enumerate(qp.variables)}
    n = int(qp.get_num_vars() ** 0.5)

    decoded_route = decode_route(best_bitstring, n, var_map)

    return decoded_route, counts
