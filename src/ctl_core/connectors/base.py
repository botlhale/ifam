from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol
import pandas as pd


@dataclass
class QuerySpec:
    select: list[str] | None = None
    where: dict[str, Any] | None = None
    limit: int | None = None


class Connector(Protocol):
    name: str

    def query(self, spec: QuerySpec) -> pd.DataFrame:
        ...