from __future__ import annotations
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
import pandas as pd

from ctl_core.registry import (
    list_connectors,
    list_transforms,
    build_connector,
    build_transform,
)
from ctl_core.connectors.base import QuerySpec
from ctl_core.fame_syntax import parse_fame_like, to_query_spec
from .models import QueryRequest, TransformRequest, FameRequest
from .deps import get_auth_user

app = FastAPI(title="CTL API", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/connectors")
async def connectors(user=Depends(get_auth_user)):
    return {"connectors": list_connectors()}


@app.get("/transforms")
async def transforms(user=Depends(get_auth_user)):
    return {"transforms": list_transforms()}


@app.post("/query")
async def query(req: QueryRequest, user=Depends(get_auth_user)):
    connector = build_connector(req.connector, req.connector_config)
    df = connector.query(
        QuerySpec(select=req.query.select, where=req.query.where, limit=req.query.limit)
    )
    return JSONResponse(df.to_dict(orient="records"))


@app.post("/transform")
async def transform(req: TransformRequest, user=Depends(get_auth_user)):
    # Load input
    if req.input.data is not None:
        df = pd.DataFrame(req.input.data)
    else:
        if not req.input.connector or not req.input.query:
            return JSONResponse({"error": "Provide input data or connector+query"}, status_code=400)
        connector = build_connector(req.input.connector, req.input.connector_config)
        q = QuerySpec(
            select=req.input.query.select,
            where=req.input.query.where,
            limit=req.input.query.limit,
        )
        df = connector.query(q)

    # Apply pipeline
    for step in req.pipeline:
        t = build_transform(step.name, step.params)
        df = t.apply(df)

    return JSONResponse(df.to_dict(orient="records"))


@app.post("/fame/query")
async def fame(req: FameRequest, user=Depends(get_auth_user)):
    spec_dict = parse_fame_like(req.fame)
    q = to_query_spec(spec_dict)
    connector = build_connector(req.connector, req.connector_config)
    df = connector.query(q)
    return JSONResponse(df.to_dict(orient="records"))