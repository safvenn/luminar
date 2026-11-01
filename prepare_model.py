import gzip
import shutil
from pathlib import Path
root = Path(__file__).resolve().parent
with gzip.open(root / 'model.pkl.gz', 'rb') as source:
    with (root / 'src/ml/model.pkl').open('wb') as target:
        shutil.copyfileobj(source, target)
