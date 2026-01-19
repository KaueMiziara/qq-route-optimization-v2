import networkx as nx
import numpy as np
from scipy.spatial import distance_matrix


def create_mining_graph(
    n_nodes: int, n_blocks: int = 1
) -> tuple[nx.Graph, np.ndarray, dict[int, np.ndarray]]:
    coords = np.random.rand(n_nodes, 2) * 100
    pos = {i: coords[i] for i in range(n_nodes)}

    dist_mat = distance_matrix(coords, coords)

    G: nx.Graph = nx.complete_graph(n_nodes)
    nx.set_node_attributes(G, pos, "pos")

    edge_list = list(G.edges())
    idx_to_block = np.random.choice(len(edge_list), size=n_blocks, replace=False)

    for i in idx_to_block:
        u, v = edge_list[i]

        G.remove_edge(u, v)
        PENALTY = 9999.0
        dist_mat[u][v] = PENALTY
        dist_mat[v][u] = PENALTY

        print(f"> Road block generated between Site {u} and {v}")

    for u, v in G.edges():
        G[u][v]["weight"] = dist_mat[u][v]

    return G, dist_mat, pos


def decode_route(
    bitstring: str,
    n: int,
    variables_idx: dict[str, int],
) -> list[int]:
    bits = bitstring[::-1]
    route = [-1] * n

    for var_name, idx in variables_idx.items():
        if bits[idx] == "1":
            parts = var_name.split("_")
            site_i = int(parts[1])
            time_t = int(parts[2])

            if time_t < n:
                route[time_t] = site_i

    return route
