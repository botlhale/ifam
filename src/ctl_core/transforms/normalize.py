from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from .base import Transform


@dataclass
class Normalize(Transform):
    """
    Min-max normalization for selected numeric columns.
    """
    columns: list[str]
    name: str = "normalize"

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for c in self.columns:
            if c not in out.columns:
                continue
            series = out[c].astype(float)
            denom = (series.max() - series.min()) or 1.0
            out[c] = (series - series.min()) / denom
        return out