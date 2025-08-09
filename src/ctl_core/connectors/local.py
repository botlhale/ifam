from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import pandas as pd
from .base import Connector, QuerySpec


@dataclass
class LocalConnector(Connector):
    """
    Reads CSV or Parquet from local filesystem.
    """
    path: str
    name: str = "local"

    def query(self, spec: QuerySpec) -> pd.DataFrame:
        if self.path.endswith(".csv"):
            df = pd.read_csv(self.path)
        elif self.path.endswith(".parquet"):
            df = pd.read_parquet(self.path)
        else:
            raise ValueError("Unsupported file type. Use .csv or .parquet")

        if spec.select:
            cols = [c for c in spec.select if c in df.columns]
            df = df[cols]

        if spec.where:
            for k, v in spec.where.items():
                if k not in df.columns:
                    continue
                df = df[df[k] == v]

        if spec.limit:
            df = df.head(spec.limit)
        return df.reset_index(drop=True)