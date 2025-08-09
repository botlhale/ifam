# Security

- Authentication
  - Dev: CTL_AUTH_MODE=disabled
  - Prod: CTL_AUTH_MODE=azure_ad
    - Validate JWTs against tenant JWKS
    - Enforce audience (AZURE_AD_AUDIENCE)
- Authorization
  - Start with coarse-grained allowlist per connector/dataset.
  - Evolve to ABAC/RBAC using app roles and group claims (e.g., roles: economist, ds, admin).
- Secrets
  - Never commit secrets; use Key Vault or secret manager.
  - Local dev with `.env`, ignored by git.
- Network
  - HTTPS only.
  - Private networking to data sources where possible.
- Auditability
  - Log queries (with redaction), transformations, and responses (metadata only).
  - Emit structured logs and traces (OpenTelemetry).