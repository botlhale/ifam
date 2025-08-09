from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

try:
    import statsmodels.api as sm
except Exception:  # pragma: no cover
    sm = None  # type: ignore

from .base import Transform


@dataclass
class SeasonalAdjustment(Transform):
    """
    Very simple seasonal adjustment using STL decomposition, requires statsmodels.
    """
    column: str
    period: int
    name: str = "seasonal_adjustment"

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if sm is None:
            raise RuntimeError("statsmodels not installed. Install with 'pip install .[stats]'")
        out = df.copy()
        if self.column not in out.columns:
            return out
        series = pd.to_numeric(out[self.column], errors="coerce").fillna(method="ffill")
        stl = sm.tsa.STL(series, period=self.period, robust=True).fit()
        out[f"{self.column}_sa"] = series - stl.seasonal
        return out