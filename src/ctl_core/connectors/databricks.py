from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

try:
    from databricks import sql as dbsql
except Exception:  # pragma: no cover
    dbsql = None  # type: ignore

from .base import Connector, QuerySpec


@dataclass
class DatabricksConnector(Connector):
    """
    Stub connector for Databricks SQL Warehouse / Unity Catalog via databricks-sql-connector.
    You must provide hostname, http_path, and access_token (or use AAD passthrough if configured).
    """
    server_hostname: str
    http_path: str
    access_token: str
    table: str
    name: str = "databricks"

    def query(self, spec: QuerySpec) -> pd.DataFrame:
        if dbsql is None:
            raise RuntimeError(
                "databricks-sql-connector not installed. Install with 'pip install .[databricks]'"
            )
        cols = ", ".join(spec.select) if spec.select else "*"
        where_clause = ""
        params = {}
        if spec.where:
            pairs = []
            for k, v in spec.where.items():
                pairs.append(f"{k} = '{v}'")
            where_clause = " WHERE " + " AND ".join(pairs)
        limit_clause = f" LIMIT {spec.limit}" if spec.limit else ""
        query = f"SELECT {cols} FROM {self.table}{where_clause}{limit_clause}"
        with dbsql.connect(
            server_hostname=self.server_hostname,
            http_path=self.http_path,
            access_token=self.access_token,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                cols_out = [c[0] for c in cursor.description]
        return pd.DataFrame(rows, columns=cols_out)