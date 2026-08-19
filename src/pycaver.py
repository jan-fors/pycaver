import sys
sys.dont_write_bytecode = True

import argparse
import os
import json

import subprocess
import uuid
import shutil
import sys

sys.path.append('/home/jan/hiwi/PyCaver/utils/parser')
import tunnel_profile_parser
import tunnel_characteristics_parser
import tunnel_residue_parser

sys.path.append('/home/jan/hiwi/PyCaver/utils/tunnel')
from Tunnel import Tunnel
from TunnelPoint import TunnelPoint
from MetaTunnel import MetaTunnel
from TunnelUtils import TunnelUtils
from CustomEncoder import CustomEncoder

import shlex

CONFIG_SAMPLE = """

"""

def caver_input_complete(caver_folder : str) -> bool:
    # check if the caver folder exists
    if not os.path.exists(caver_folder):
        print(f"Error: The specified path does not exist: {args.caver}")
        return False
    # create the path to the caver.jar file
    caver_jar = os.path.join(caver_folder, "caver.jar")
    # check if the caver.jar file exists
    if not os.path.exists(caver_jar):
        print(f"Error: The caver.jar file does not exist in the specified path: {args.caver}")
        return False
    # create the path to the lib-directory
    lib_path = os.path.join(caver_folder, "lib")
    # check if the lib-directory exists
    if not os.path.exists(lib_path):
        print(f"Error: The lib-directory does not exist in the specified path: {args.caver}")
        return False
    return True

def create_configuration(probe_radius : float, shell_radius : float, shell_depth : float, starting_point_coordinates : tuple, desired_radius : float, max_distance : float) -> str:
    """
    Create a configuration file for CAVER
    """
    starting_point_coordinates = " ".join([str(x) for x in starting_point_coordinates])
    res = CONFIG_SAMPLE + "\n"
    res += f"""
            #*****************************
            # TUNNEL CALCULATION
            #*****************************
            probe_radius {probe_radius}
            shell_radius {shell_radius}
            shell_depth {shell_depth}

            starting_point_coordinates {starting_point_coordinates}

            #-----------------------------
            # Starting point optimization
            #-----------------------------
            desired_radius {desired_radius}
            max_distance {max_distance}
            """
    return res

def list_of_floats(arg):
    try:
        return [float(x) for x in arg.split(',')]
    except:
        raise argparse.ArgumentTypeError("Coordinates must be a list of floats separated by commas")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyCaver: A Python-wrapper for CAVER, a software tool for the analysis and visualization of tunnels and channels in protein structures.')
    parser.add_argument('-i', '--input', help='Input file', required=True)
    parser.add_argument('-o', '--output', help='Output file', required=True)
    parser.add_argument('-c', '--caver', help='Path to the CAVER folder containing the caver.jar file and the lib-directory', default="caver_3.0/caver")

    parser.add_argument('-t', '--tmp', help='Temporary folder for storing temporary files"', default="tmp")
    parser.add_argument('-hs', '--heapSize', help='Heap size for Java', default=4000)
    parser.add_argument('-n', '--name', help='Name of the output file', default=None)

    parser.add_argument('--pdb_wise', help='PDB-wise mode', action='store_true')

    parser.add_argument('-G', '--graph', help='Generate a graph of the tunnel', action='store_true')

    parser.add_argument('--verbose', help='Verbose output', action='store_true')

    # parser.add_argument('--print-summary', help='Print a summary of the results', action='store_true')

    #################################### caver options ####################################
    parser.add_argument('--probe-radius',type=float, help='Probe radius [0.9]', default=0.9)
    parser.add_argument('--shell-radius',type=float, help='Shell radius [3.0]', default=3.0)
    parser.add_argument('--shell-depth',type=float, help='Shell depth [4.0]', default=4.0)
    parser.add_argument('-x', type=float, help='X-coordinate of the starting point [0.0]', default=0.0)
    parser.add_argument('-y', type=float, help='Y-coordinate of the starting point [0.0]', default=0.0)
    parser.add_argument('-z', type=float, help='Z-coordinate of the starting point [0.0]', default=0.0)
    parser.add_argument('--starting-point-coordinates', type=float, nargs=3, help='Coordinates of the starting point as a list of floats [0.0, 0.0, 0.0]', default=None)
    parser.add_argument('--desired-radius', type=float, help='Desired radius for the starting point optimization [5.0]', default=5.0)
    parser.add_argument('--max-distance', type=float, help='Maximum distance for the starting point optimization [3.0]', default=3.0)
    #################################### caver options ####################################

    args = parser.parse_args()

    if args.starting_point_coordinates is None:
        # if no starting point coordinates are given, use the x, y, z coordinates
        starting_point_coordinates = (args.x, args.y, args.z)
    else:
        starting_point_coordinates = tuple(args.starting_point_coordinates)
    
    if args.verbose:
        print("Verbose mode enabled")
        print(f"Input file: {args.input}")
        print(f"Output file: {args.output}")
        print(f"CAVER folder: {args.caver}")
        print(f"Temporary folder: {args.tmp}")
        print(f"Heap size: {args.heapSize} MB")
        print(f"Name: {args.name}")
        print(f"PDB-wise mode: {args.pdb_wise}")
        print(f"Generate graph: {args.graph}")
        print(f"Probe radius: {args.probe_radius}")
        print(f"Shell radius: {args.shell_radius}")
        print(f"Shell depth: {args.shell_depth}")
        print(f"Starting point coordinates: {starting_point_coordinates}")
        print(f"Desired radius: {args.desired_radius}")
        print(f"Maximum distance: {args.max_distance}")

    # perform caver input checks
    if not caver_input_complete(args.caver):
        exit()
    else:
        caver_jar = os.path.join(args.caver, "caver.jar")
        caver_lib = os.path.join(args.caver, "lib")

    # check if tmp folder exists
    if not os.path.exists(args.tmp):
        os.makedirs(args.tmp)
        print(f"Created temporary folder: {args.tmp}")

    # check if output folder exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        print(f"Created output folder: {args.output}")

    # check if name is defined if not create custom id
    if args.name is None:
        name = str(uuid.uuid4())
    else:
        name = args.name

    # check if input is file or directory
    if os.path.isdir(args.input):       # Input is directory
        if args.pdb_wise:            # PDB-wise mode is enabled
            """
            Running caver in PDB-wise mode meaning caver will be run for each PDB file in the input directory
            - therefore separat folders have to be created in the tmp folder for each PDB file
            - the pdb files will get copied there
            - caver is run on each folder and the results are stored in the output folder in one subfolder for each pdb file
            """
            pass
            

        else:
            """
            Running caver in normal mode meaning caver will be run on the input directory
            - therefore no folder has to be created in the tmp folder OR save the config file in the tmp folder??
            - output is stored in the output folder
            """
            pass


    elif os.path.isfile(args.input):    # Input is single file
        """
        Running caver in single file mode meaning caver will be run on the input file
        - therefore a folder has to be created in the tmp folder
        - the pdb file will get copied there
        - caver is run on the folder and the results are stored in the output folder
        """
        # prepare folder
        name_folder = os.path.join(args.tmp, name)
        if not os.path.exists(name_folder):
            os.makedirs(name_folder)

        out_folder = os.path.join(args.output, name)
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        in_folder = os.path.join(name_folder, "input")
        os.makedirs(in_folder)

        # copy pdb file to folder
        pdb_file_source = os.path.join(args.input)
        pdb_file_name = os.path.basename(pdb_file_source)
        pdb_file_destination = os.path.join(in_folder, pdb_file_name)

        try:
            shutil.copy(pdb_file_source, pdb_file_destination)
            #verbose print("File copied successfully.")
        except shutil.SameFileError:
            print("Error: Source and destination represents the same file.")
            exit()
        except PermissionError:
            print("Error: Permission denied.")
            exit()
        except:
            print("Error occurred while copying file.")
            exit()

        # create config file
        config_file = os.path.join(name_folder, "config.txt")
        with open(config_file, "w") as file:
            config = create_configuration(probe_radius=args.probe_radius, shell_radius=args.shell_radius, shell_depth=args.shell_depth, starting_point_coordinates=starting_point_coordinates, desired_radius=args.desired_radius, max_distance=args.max_distance)
            file.write(config)

        # run caver
        print(f"Running CAVER on {pdb_file_name}")
        execute_caver(heapSize=args.heapSize, caver_lib=caver_lib, caver_jar=caver_jar, caver_folder=args.caver, pdb_folder=in_folder, config=config_file, output_folder=out_folder)

        # create graph representation
        if args.graph:
            # create path to tunnel_profiles.csv
            tunnel_profiles = os.path.join(out_folder, "analysis", "tunnel_profiles.csv")
            tunnel_characteristics = os.path.join(out_folder, "analysis", "tunnel_characteristics.csv")
            residue_file = os.path.join(out_folder, "analysis", "residues.txt")
            # check if the path exists
            if os.path.isfile(tunnel_profiles):
                tunnel_profile_data = tunnel_profile_parser.parse_tunnel_profiles(tunnel_profiles)
                
                """
                The tunnel profile data is used to extract the tunnel points which are added to the corresponding tunnels.
                The tunnel objects are then saved
                """
                tunnel_obj = []
                for t in tunnel_profile_data.keys():
                    tunnel = Tunnel(t)
                    tunnel.add_root(TunnelPoint(tunnel_profile_data[t]["x"][0], tunnel_profile_data[t]["y"][0], tunnel_profile_data[t]["z"][0], tunnel_profile_data[t]["r"][0]))
                    for i in range(1,len(tunnel_profile_data[t]["x"])):
                        tunnel.add_TunnelPoint(TunnelPoint(tunnel_profile_data[t]["x"][i], tunnel_profile_data[t]["y"][i], tunnel_profile_data[t]["z"][i], tunnel_profile_data[t]["r"][i]))
                    tunnel_obj.append(tunnel)

                """
                Create the meta tunnel
                """
                m = MetaTunnel()

                m.add_first(tunnel_obj[0])
                for t in tunnel_obj[1:]:
                    m = TunnelUtils.merge(tunnel=t, meta_tunnel=m)

                # print the meta tunnel
                m.iplot(os.path.join(out_folder, "tunnel.html"))
                m.write_graph_to_json(os.path.join(out_folder, "graph.json"))

                # instead of saving the meta-tunnel.json -> use the other parts like residue data and characteristics and concat everything
                metatunnel_data = m.get_meta_data()

                """
                we want the tunnel length and curvature
                """
                tunnel_characteristics_data = tunnel_characteristics_parser.parse_tunnel_characteristics_summary(tunnel_characteristics)
                      
                """
                we want a fingerprint of the n aa next to the active site
                """
                residue_data = tunnel_residue_parser.parse_tunnel_residue_summary(residue_file)

                # Combine the dictionaries into a single result dictionary
                combined_data = {}
                combined_data.update(metatunnel_data)
                combined_data.update(tunnel_characteristics_data)
                combined_data.update(residue_data)

                # Optionally, print or save the combined data
                if args.verbose:
                    for k in combined_data.keys():
                        print(k,":::", combined_data[k])

                with open(os.path.join(out_folder, "meta-tunnel.json"), "w") as f:
                    json.dump(combined_data, f, indent=4, cls=CustomEncoder)
      
            else:
                print("Error: The tunnel_profiles.csv file does not exist")
                exit()
            pass

    else:
        print("Error: The specified input is neither a file nor a directory")
        exit()
    
