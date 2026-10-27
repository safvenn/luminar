from pathlib import Path
import pandas as pd


class DataRepository:
    def __init__(self, data_path: str | None = None):
        if data_path is None:
            data_path = str(Path(__file__).resolve().parents[2] / "uploads" / "diabetes.csv")
        self.data_path = Path(data_path)

    def get_dataset(self) -> pd.DataFrame:
        return pd.read_csv(self.data_path)