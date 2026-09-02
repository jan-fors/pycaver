from pycaver.utils.paths import get_data_dir
from pycaver.utils.fetch import fetch_caver

def init(force: bool = False):
    data_dir = get_data_dir()
    fetch_caver(data_dir, force=force)
    print("CAVER installed and ready.")