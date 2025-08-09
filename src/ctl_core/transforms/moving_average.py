from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from .base import Transform


@dataclass
class MovingAverage(Transform):
    column: str
    window: int = 3
    name: str = "moving_average"

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        if self.column in out.columns:
            out[f"{self.column}_ma{self.window}"] = (
                out[self.column].astype(float).rolling(self.window, min_periods=1).mean()
            )
        return out