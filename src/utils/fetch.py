import zipfile
import urllib.request
from pathlib import Path

CAVER_URL = "https://www.caver.cz/fil/download/caver30/302/caver_3.0.2.zip" 

def fetch_caver(dest_dir: Path, force: bool = False) -> Path:
    install_dir = dest_dir / "prog" / "caver_3.0"
    marker = install_dir / ".installed"

    if marker.exists() and not force:
        return install_dir

    install_dir.parent.mkdir(parents=True, exist_ok=True)
    archive_path = dest_dir / "caver_archive.zip"

    print(f"Downloading CAVER from {CAVER_URL} ...")
    urllib.request.urlretrieve(CAVER_URL, archive_path)

    print(f"Extracting to {install_dir} ...")
    with zipfile.ZipFile(archive_path) as zf:
        zf.extractall(install_dir)

    archive_path.unlink()
    marker.touch()
    return install_dir