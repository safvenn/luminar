import gzip
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
target_dir = root / "src" / "ml"
target_dir.mkdir(parents=True, exist_ok=True)
gz_path = root / "model.pkl.gz"
if gz_path.exists():
    with gzip.open(gz_path, "rb") as source:
        with (target_dir / "model.pkl").open("wb") as target:
            shutil.copyfileobj(source, target)
