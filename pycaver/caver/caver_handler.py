import subprocess
from pathlib import Path
from pycaver.utils.constants import (
    HEAP_SIZE,
)
from pycaver.utils.paths import get_caver_paths

def execute_caver(pdb_folder : Path, config : Path, output_folder : Path):
    """
    use subprocess to run caver
    """
    paths = get_caver_paths()
    cmd = ["java", f"-Xmx{str(HEAP_SIZE)}m", "-cp", str(paths["CAVER_LIB"]), "-jar", str(paths["CAVER_JAR"]), "-home", str(paths["CAVER_FOLDER"]), "-pdb", str(pdb_folder), "-conf", str(config), "-out", str(output_folder)]
    print(f"Executing command: {' '.join(cmd)} ...")
    subprocess.run(cmd, capture_output=True, text=True)
    print("... done")