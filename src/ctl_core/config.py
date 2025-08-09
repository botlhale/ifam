from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    auth_mode: str = os.getenv("CTL_AUTH_MODE", "disabled")
    azure_tenant_id: str | None = os.getenv("AZURE_AD_TENANT_ID")
    azure_audience: str | None = os.getenv("AZURE_AD_AUDIENCE")

    # Example connection strings (for demos; use Key Vault in prod)
    azure_sql_url: str | None = os.getenv("AZURE_SQL_URL")
    mysql_url: str | None = os.getenv("MYSQL_URL")

    api_host: str = os.getenv("CTL_API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("CTL_API_PORT", "8000"))


settings = Settings()