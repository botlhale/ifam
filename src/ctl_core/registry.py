from __future__ import annotations
from typing import Callable, Dict

from .connectors.base import Connector
from .connectors.local import LocalConnector
from .connectors.azure_sql import AzureSqlConnector
from .connectors.mysql import MySqlConnector
from .connectors.databricks import DatabricksConnector

from .transforms.base import Transform
from .transforms.normalize import Normalize
from .transforms.moving_average import MovingAverage
from .transforms.seasonal_adjustment import SeasonalAdjustment


# Factories to instantiate connectors/transforms from dict configs
ConnectorFactory = Callable[[dict], Connector]
TransformFactory = Callable[[dict], Transform]

connectors: Dict[str, ConnectorFactory] = {
    "local": lambda cfg: LocalConnector(**cfg),
    "azure_sql": lambda cfg: AzureSqlConnector(**cfg),
    "mysql": lambda cfg: MySqlConnector(**cfg),
    "databricks": lambda cfg: DatabricksConnector(**cfg),
}

transforms: Dict[str, TransformFactory] = {
    "normalize": lambda cfg: Normalize(**cfg),
    "moving_average": lambda cfg: MovingAverage(**cfg),
    "seasonal_adjustment": lambda cfg: SeasonalAdjustment(**cfg),
}


def build_connector(name: str, cfg: dict) -> Connector:
    if name not in connectors:
        raise KeyError(f"Unknown connector: {name}")
    return connectors[name](cfg)


def build_transform(name: str, cfg: dict) -> Transform:
    if name not in transforms:
        raise KeyError(f"Unknown transform: {name}")
    return transforms[name](cfg)


def list_connectors() -> list[str]:
    return sorted(connectors.keys())


def list_transforms() -> list[str]:
    return sorted(transforms.keys())