from pathlib import Path
from src.utils.constants import BASE_CONFIG_PATH


def build_config(
    output_dir: Path,
    probe_radius: float,
    shell_radius: float,
    shell_depth: float,
    starting_point_coordinates: tuple,
    desired_radius: float,
    max_distance: float,
) -> Path:
    """
    Creates a custom config file inside the output dir and returns the path to this file
    """
    # read base config
    with open(BASE_CONFIG_PATH, "r") as f:
        lines = f.read()

    # append relevant lines
    lines += f"""
#*****************************
# TUNNEL CALCULATION
#*****************************
probe_radius {probe_radius}
shell_radius {shell_radius}
shell_depth {shell_depth}

starting_point_coordinates {" ".join([str(x) for x in starting_point_coordinates])}

#-----------------------------
# Starting point optimization
#-----------------------------
desired_radius {desired_radius}
max_distance {max_distance}
            """

    output_path = output_dir / Path("config.txt")
    with open(output_path, "w") as f:
        f.write(lines)

    return output_path
