from __future__ import annotations
import re
from typing import Any, Dict
from .connectors.base import QuerySpec


def parse_fame_like(expr: str) -> Dict[str, Any]:
    """
    Extremely simplified FAME-like syntax:
    Example: "SELECT date,series,value FROM table WHERE series=GDP LIMIT 100"
    Returns dict approximation usable by QuerySpec.
    """
    m_select = re.search(r"SELECT\s+(?P<select>.+?)\s+FROM", expr, re.IGNORECASE)
    m_where = re.search(r"WHERE\s+(?P<where>.+?)(\s+LIMIT|\s*$)", expr, re.IGNORECASE)
    m_limit = re.search(r"LIMIT\s+(?P<limit>\d+)", expr, re.IGNORECASE)

    select_cols = None
    if m_select:
        cols = [c.strip() for c in m_select.group("select").split(",")]
        select_cols = cols if "*" not in cols else None

    where = None
    if m_where:
        where = {}
        parts = re.split(r"\s+AND\s+", m_where.group("where"), flags=re.IGNORECASE)
        for p in parts:
            kv = re.split(r"\s*=\s*", p, maxsplit=1)
            if len(kv) == 2:
                where[kv[0].strip()] = kv[1].strip().strip("'").strip('"')

    limit = int(m_limit.group("limit")) if m_limit else None
    return {"select": select_cols, "where": where, "limit": limit}


def to_query_spec(d: Dict[str, Any]) -> QuerySpec:
    return QuerySpec(
        select=d.get("select"), where=d.get("where"), limit=d.get("limit")
    )