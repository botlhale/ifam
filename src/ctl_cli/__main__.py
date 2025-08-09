from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

import pandas as pd
import typer

from ctl_core.registry import build_connector, build_transform
from ctl_core.connectors.base import QuerySpec

app = typer.Typer(help="CTL Command Line Interface")


@app.command()
def query(
    connector: str = typer.Argument(..., help="Connector name (e.g., local, azure_sql)"),
    path: Optional[str] = typer.Option(None, help="For local connector, file path"),
    table: Optional[str] = typer.Option(None, help="For SQL connectors, table name"),
    url: Optional[str] = typer.Option(None, help="SQLAlchemy URL for SQL connectors"),
    where: list[str] = typer.Option(None, help="Filters like key=value"),
    select: list[str] = typer.Option(None, help="Columns to select"),
    limit: Optional[int] = typer.Option(None, help="Row limit"),
):
    cfg = {}
    if connector == "local" and path:
        cfg["path"] = path
    if connector in {"azure_sql", "mysql"}:
        if url:
            cfg["url"] = url
        if table:
            cfg["table"] = table

    spec_where = {}
    if where:
        for w in where:
            k, v = w.split("=", 1)
            spec_where[k] = v

    conn = build_connector(connector, cfg)
    df = conn.query(QuerySpec(select=select or None, where=spec_where or None, limit=limit))
    typer.echo(df.to_csv(index=False))


@app.command()
def transform(
    in_: str = typer.Option(..., "--in", help="Input CSV file"),
    out: Optional[str] = typer.Option(None, help="Output CSV file (default: stdout)"),
    pipeline: list[str] = typer.Option(
        None,
        help="Pipeline steps like normalize:columns=value moving_average:column=value,window=3",
    ),
):
    df = pd.read_csv(in_)
    for step in pipeline or []:
        name, _, args = step.partition(":")
        params = {}
        if args:
            for pair in args.split(","):
                k, v = pair.split("=", 1)
                # try casting to int/float
                if v.isdigit():
                    v_parsed = int(v)
                else:
                    try:
                        v_parsed = float(v)
                    except ValueError:
                        if v == "true":
                            v_parsed = True
                        elif v == "false":
                            v_parsed = False
                        else:
                            v_parsed = v
                # support list columns=value1|value2
                if "|" in str(v_parsed):
                    v_parsed = v_parsed.split("|")
                params[k] = v_parsed
        t = build_transform(name, params)
        df = t.apply(df)

    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out, index=False)
    else:
        typer.echo(df.to_csv(index=False))


if __name__ == "__main__":
    app()