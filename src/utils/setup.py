from mypkg.paths import get_data_dir
from mypkg.fetch import fetch_caver

def init(force: bool = False):
    data_dir = get_data_dir()
    fetch_caver(data_dir, force=force)
    print("CAVER installed and ready.")