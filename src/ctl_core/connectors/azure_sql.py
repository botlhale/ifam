from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import pandas as pd

try:
    from sqlalchemy import create_engine, text
except Exception:  # pragma: no cover
    create_engine = None  # type: ignore

from .base import Connector, QuerySpec


@dataclass
class AzureSqlConnector(Connector):
    """
    Template connector using SQLAlchemy. Provide a SQLAlchemy URL.
    Example:
      mssql+pyodbc://user:pass@server.database.windows.net:1433/db?driver=ODBC+Driver+18+for+SQL+Server
    """
    url: str
    table: str
    name: str = "azure_sql"

    def query(self, spec: QuerySpec) -> pd.DataFrame:
        if create_engine is None:
            raise RuntimeError("SQLAlchemy not installed. Install with 'pip install .[sql]'")
        engine = create_engine(self.url)
        cols = ", ".join(spec.select) if spec.select else "*"
        where_clause = ""
        params = {}
        if spec.where:
            where_parts = []
            for i, (k, v) in enumerate(spec.where.items()):
                p = f"p{i}"
                where_parts.append(f"{k} = :{p}")
                params[p] = v
            where_clause = " WHERE " + " AND ".join(where_parts)

        limit_clause: str = f" TOP {spec.limit} " if spec.limit else ""
        sql = text(f"SELECT {limit_clause}{cols} FROM {self.table}{where_clause}")
        with engine.connect() as conn:
            df = pd.read_sql(sql, conn, params=params)
        return df