from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field


class QueryModel(BaseModel):
    select: Optional[List[str]] = None
    where: Optional[Dict[str, Any]] = None
    limit: Optional[int] = None


class QueryRequest(BaseModel):
    connector: str
    connector_config: Dict[str, Any] = Field(default_factory=dict)
    query: QueryModel


class TransformStep(BaseModel):
    name: str
    params: Dict[str, Any] = Field(default_factory=dict)


class InputSource(BaseModel):
    # Either provide inline data rows, or a connector+query
    data: Optional[list[dict[str, Any]]] = None
    connector: Optional[str] = None
    connector_config: Dict[str, Any] = Field(default_factory=dict)
    query: Optional[QueryModel] = None


class TransformRequest(BaseModel):
    input: InputSource
    pipeline: List[TransformStep]


class FameRequest(BaseModel):
    connector: str
    connector_config: Dict[str, Any] = Field(default_factory=dict)
    fame: str