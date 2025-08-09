from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Any
import pandas as pd


@dataclass
class TransformConfig:
    params: dict[str, Any]


class Transform(Protocol):
    name: str

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        ...