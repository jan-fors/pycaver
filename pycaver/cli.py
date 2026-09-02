""" """

import argparse
from pathlib import Path
import os
from pycaver.main import main
import shutil
from pycaver.utils.constants import (
    SHELL_RADIUS,
    SHELL_DEPTH,
    PROBE_RADIUS,
    DESIRED_RADIUS,
    MAX_DISTANCE,
)
from pycaver.utils.setup import init

def _extract_inputs(args):
    """ """
    return (
        args.input,
        args.output_dir,
        args.shell_radius,
        args.shell_depth,
        args.probe_radius,
        args.desired_radius,
        args.max_distance,
        args.starting_point_coordinates
    )

def cli(args):
    """ """
    # check setup
    init()
    
    # extract inputs
    (
        input,
        output_dir,
        shell_radius,
        shell_depth,
        probe_radius,
        desired_radius,
        max_distance,
        starting_point_coordinates
    ) = _extract_inputs(args)

    # check inputs
    # TODO

    # create output folder
    output_path = output_dir / Path(input.stem)
    os.makedirs(output_path, exist_ok=True)

    input_folder = output_path / Path("in")
    os.makedirs(input_folder, exist_ok=True)
    shutil.copy2(input, input_folder)

    # main
    main(
        input_folder=input_folder,
        output_dir=output_path,
        shell_radius=shell_radius,
        shell_depth=shell_depth,
        probe_radius=probe_radius,
        desired_radius=desired_radius,
        max_distance=max_distance,
        starting_point_coordinates=starting_point_coordinates
    )


def entry():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("input", type=Path, help="Path to a structure file (pdb).")
    parser.add_argument(
        "-o", "--output_dir", type=Path, help="Path to the output directory.", default="."
    )

    parser.add_argument("--shell_radius", type=float, default=SHELL_RADIUS)
    parser.add_argument("--shell_depth", type=float, default=SHELL_DEPTH)
    parser.add_argument("--probe_radius", type=float, default=PROBE_RADIUS)
    parser.add_argument("--desired_radius", type=float, default=DESIRED_RADIUS)
    parser.add_argument("--max_distance", type=float, default=MAX_DISTANCE)

    parser.add_argument("--starting_point_coordinates", nargs=3, type=float, metavar=("X", "Y", "Z"),
                    help="3D coordinates as three floats: X Y Z)", required=True)

    args = parser.parse_args()

    cli(args)


if __name__ == "__main__":
    entry()