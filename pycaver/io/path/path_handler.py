from pathlib import Path
import os

def get_result_paths(result_dir : Path) -> tuple[Path, Path, Path]:
    """
    """
    tunnel_profiles_path = result_dir / Path("analysis") / Path("tunnel_profiles.csv")
    if not os.path.exists(tunnel_profiles_path):
        print(f"Path {tunnel_profiles_path} does not exist.")
        tunnel_profiles_path = None
    
    tunnel_characteristics_path = result_dir / Path("analysis") / Path("tunnel_characteristics.csv")
    if not os.path.exists(tunnel_characteristics_path):
        print(f"Path {tunnel_characteristics_path} does not exist.")
        tunnel_characteristics_path = None

    residue_file_path = result_dir / Path("analysis") / Path("residues.txt")
    if not os.path.exists(residue_file_path):
        print(f"Path {residue_file_path} does not exist.")
        residue_file_path = None

    return tunnel_profiles_path, tunnel_characteristics_path, residue_file_path