import subprocess
from pathlib import Path
from src.utils.constants import (
    HEAP_SIZE,
    CAVER_LIB,
    CAVER_JAR,
    CAVER_FOLDER
)

def execute_caver(pdb_folder : Path, config : Path, output_folder : Path):
    """
    use subprocess to run caver
    """
    cmd = ["java", f"-Xmx{str(HEAP_SIZE)}m", "-cp", str(CAVER_LIB), "-jar", str(CAVER_JAR), "-home", str(CAVER_FOLDER), "-pdb", str(pdb_folder), "-conf", str(config), "-out", str(output_folder)]
    print(f"Executing command: {' '.join(cmd)} ...")
    subprocess.run(cmd, capture_output=True, text=True)
    print("... done")