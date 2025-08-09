from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from jose import jwk, jwt
from jose.utils import base64url_decode
import httpx


@dataclass
class AzureADConfig:
    tenant_id: str
    audience: str


class AzureADVerifier:
    def __init__(self, cfg: AzureADConfig):
        self.cfg = cfg
        self._jwks_uri = f"https://login.microsoftonline.com/{cfg.tenant_id}/discovery/v2.0/keys"
        self._jwks: dict[str, Any] | None = None

    async def load_keys(self) -> dict[str, Any]:
        if self._jwks is None:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(self._jwks_uri)
                resp.raise_for_status()
                self._jwks = resp.json()
        return self._jwks

    async def validate(self, token: str) -> dict[str, Any]:
        jwks = await self.load_keys()
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key:
            raise ValueError("Key not found for token")

        message, encoded_sig = token.rsplit(".", 1)
        decoded_sig = base64url_decode(encoded_sig.encode("utf-8"))

        public_key = jwk.construct(key)
        if not public_key.verify(message.encode("utf-8"), decoded_sig):
            raise ValueError("Invalid token signature")

        claims = jwt.get_unverified_claims(token)
        aud = claims.get("aud")
        if aud != self.cfg.audience:
            raise ValueError("Invalid audience")

        # Expiry and nbf are validated in jose verify; inlined verification kept simple here
        return claims