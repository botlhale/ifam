from __future__ import annotations
from fastapi import Header, HTTPException
from ctl_core.config import settings
from ctl_core.auth.azure_ad import AzureADConfig, AzureADVerifier


async def get_auth_user(authorization: str | None = Header(default=None)) -> dict | None:
    if settings.auth_mode == "disabled":
        return None  # dev mode
    if settings.auth_mode == "azure_ad":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing Bearer token")
        token = authorization.split(" ", 1)[1]
        if not (settings.azure_tenant_id and settings.azure_audience):
            raise HTTPException(status_code=500, detail="Azure AD not configured")
        verifier = AzureADVerifier(
            AzureADConfig(tenant_id=settings.azure_tenant_id, audience=settings.azure_audience)
        )
        try:
            claims = await verifier.validate(token)
            return claims
        except Exception as e:  # pragma: no cover
            raise HTTPException(status_code=401, detail=str(e))
    raise HTTPException(status_code=500, detail=f"Unknown auth mode {settings.auth_mode}")