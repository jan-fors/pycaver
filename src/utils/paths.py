from pathlib import Path
from platformdirs import user_data_dir

APP_NAME = "pycaver"

def get_data_dir() -> Path:
    d = Path(user_data_dir(APP_NAME))
    d.mkdir(parents=True, exist_ok=True)
    return d

def get_caver_paths() -> dict:
    caver_folder = get_data_dir() / "prog" / "caver_3.0" / "caver"
    return {
        "CAVER_FOLDER": caver_folder,
        "CAVER_LIB": caver_folder / "lib",
        "CAVER_JAR": caver_folder / "caver.jar",
    }