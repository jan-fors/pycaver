from pathlib import Path
from typing import List
from src.caver.build_config import build_config
from src.caver.caver_handler import execute_caver
from src.io.parser.tunnel_profile_parser import parse_tunnel_profiles
from src.io.parser.tunnel_characteristics_parser import (
    parse_tunnel_characteristics_summary,
)
from src.io.parser.tunnel_residue_parser import parse_tunnel_residue_summary
from src.io.path.path_handler import get_result_paths
from src.tunnel.Tunnel import build_tunnels
from src.tunnel.MetaTunnel import MetaTunnel, build_metatunnel
from src.io.writers.output_summary import write_outputs


def main(
    input_folder: Path,
    output_dir: Path,
    shell_radius: float,
    shell_depth: float,
    probe_radius: float,
    desired_radius: float,
    max_distance: float,
    starting_point_coordinates: List[float],
):
    """ """
    # create caver config file
    config_path = build_config(
        output_dir=output_dir,
        probe_radius=probe_radius,
        shell_radius=shell_radius,
        shell_depth=shell_depth,
        starting_point_coordinates=starting_point_coordinates,
        desired_radius=desired_radius,
        max_distance=max_distance,
    )

    # execute caver
    execute_caver(pdb_folder=input_folder, config=config_path, output_folder=output_dir)

    # parse caver outputs
    tunnel_profiles_path, tunnel_characteristics_path, residue_file_path = (
        get_result_paths(output_dir)
    )

    if any(
        x == None
        for x in [tunnel_profiles_path, tunnel_characteristics_path, residue_file_path]
    ):
        print("Cannot create meta-tunnel.")
        exit(0)  # TODO is this a problem for high throughput?

    tunnel_profiles = parse_tunnel_profiles(tunnel_profiles_path)
    tunnel_characteristics = parse_tunnel_characteristics_summary(
        tunnel_characteristics_path
    )
    tunnel_residues = parse_tunnel_residue_summary(residue_file_path)

    # create tunnel object
    tunnel_objs = build_tunnels(tunnel_profiles)

    meta_tunnel = build_metatunnel(tunnel_objs)  # creates all relevant measurments

    # save
    write_outputs(
        output_dir=output_dir,
        meta_tunnel=meta_tunnel,
        tunnel_characteristics=tunnel_characteristics,
        residue_data=tunnel_residues,
    )
