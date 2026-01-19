import matplotlib.pyplot as plt

from route_optimization.logger import Logger
from route_optimization.visualization import open_image_external, save_plot


def plot_convergence(log: Logger):
    plt.figure(figsize=(10, 5))
    plt.plot(log.counts, log.values, color="purple", label="VQE Energy")
    plt.xlabel("Interactions (Cost Evolution)")
    plt.ylabel("Energy (Hamiltonian)")
    plt.title("VQE Convergence until Optimal Route")
    plt.grid(True, alpha=0.3)
    plt.legend()

    saved_path = save_plot("convergence_plot")
    print(f"\nSaved plot: {saved_path}")
    plt.close()

    open_image_external(saved_path)
