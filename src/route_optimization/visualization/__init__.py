import os
import subprocess
import sys

import matplotlib.pyplot as plt


def save_plot(file_name: str) -> str:
    PLOTS_DIR = "./plots"
    PLOT_FILENAME = f"{PLOTS_DIR}/{file_name}.png"

    os.makedirs(PLOTS_DIR, exist_ok=True)
    plt.savefig(PLOT_FILENAME)

    return os.path.abspath(PLOT_FILENAME)


def open_image_external(path: str) -> None:
    current_os = sys.platform

    try:
        match current_os:
            case "win32":
                os.startfile(path)  # type: ignore
            case "darwin":
                subprocess.run(["open", path], check=True)
            case _:
                subprocess.run(["xdg-open", path], check=True)
    except Exception as e:
        print(f"Warning: Could not open image viewer automatically. Error: {e}")
