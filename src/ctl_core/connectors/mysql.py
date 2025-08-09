from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

try:
    from sqlalchemy import create_engine, text
except Exception:  # pragma: no cover
    create_engine = None  # type: ignore

from .base import Connector, QuerySpec


@dataclass
class MySqlConnector(Connector):
    """
    Template connector using SQLAlchemy.
    Example URL: mysql+pymysql://user:password@host:3306/dbname
    """
    url: str
    table: str
    name: str = "mysql"

    def query(self, spec: QuerySpec) -> pd.DataFrame:
        if create_engine is None:
            raise RuntimeError("SQLAlchemy not installed. Install with 'pip install .[sql]'")
        engine = create_engine(self.url)
        cols = ", ".join(spec.select) if spec.select else "*"
        where_clause = ""
        params = {}
        if spec.where:
            where_parts = []
            for k, v in spec.where.items():
                p = f"{k}"
                where_parts.append(f"{k} = :{p}")
                params[p] = v
            where_clause = " WHERE " + " AND ".join(where_parts)

        limit_clause = f" LIMIT {spec.limit}" if spec.limit else ""
        sql = text(f"SELECT {cols} FROM {self.table}{where_clause}{limit_clause}")
        with engine.connect() as conn:
            df = pd.read_sql(sql, conn, params=params)
        return df