# CTL: Common Transformation Library (Python)

CTL is a shareable Python library and API that standardizes data access and transformation for economists, statisticians, business analysts, and data scientists. It mirrors the “CTL Related Workflow” you shared:

- Data access using enterprise identity (Microsoft Entra ID/Azure AD) to sources such as Azure SQL, MySQL, Databricks, and local files.
- A reusable Common Transformation Library (CTL) that can run:
  - As a Python package for notebooks and scripts,
  - As a REST API (FastAPI) for apps, Excel, Stata, R, MATLAB, etc.
- A pluggable connector and transformation registry.
- Optional FAME-like query syntax adapter for users migrating from legacy FAME/Excel workflows.

This repo is a template: fork it, rename it, and extend it with your organization’s connectors, transformations, and deployment targets.

---

## Who is this for?

- Directors and Leadership: A consistent platform for governed, reusable data transformations, reducing duplicated effort and vendor lock-in. Observable, secure, and deployable on-prem or in cloud.
- Economists, Statisticians, Analysts: A simple, ergonomic API and CLI to access data and run transformations from Python, Excel, Stata, R, and MATLAB.
- Data Scientists and Engineers: A clean Python package with registries, configuration, tests, CI/CD, and extension points.

---

## High-level architecture

- CTL Core (Python package): connectors, transformation functions, registry, FAME-like query adapter.
- CTL API (FastAPI): a stateless REST layer exposing CTL to external tools.
- Auth: Dev mode (no auth) and production mode validating Microsoft Entra ID JWTs.
- Clients: Examples for Python, R, Stata, MATLAB, and Excel (via Python/xlwings).
- Deployment: Dockerfile, docker-compose, and CI workflow. Production guidance for Azure App Service / Container Apps with Key Vault.

---

## Quick start (local development)

Prerequisites: Python 3.10+, make, Docker (optional).

1) Create virtual environment and install:
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -U pip
pip install -e ".[dev]"    # installs CTL with dev extras
```

2) Run the API (dev mode, no auth):
```bash
make run
# or: uvicorn ctl_api.main:app --reload
```
Visit http://localhost:8000/docs for OpenAPI.

3) Try the local file connector:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "connector": "local",
    "connector_config": {"path": "data/example.csv"},
    "query": {"select": ["date","series","value"], "where": {"series": "GDP"}}
  }'
```

4) Run a transformation:
```bash
curl -X POST http://localhost:8000/transform \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "connector": "local",
      "connector_config": {"path": "data/example.csv"},
      "query": {"select": ["date","series","value"], "where": {"series": "GDP"}}
    },
    "pipeline": [
      {"name": "normalize", "params": {"columns": ["value"]}},
      {"name": "moving_average", "params": {"column": "value", "window": 3}}
    ]
  }'
```

5) CLI usage:
```bash
ctl --help
ctl query local --path data/example.csv --where series=GDP
ctl transform --in data/example.csv --pipeline normalize:columns=value moving_average:column=value,window=3
```

---

## Configuration

- .env controls runtime behavior (see .env.example).
- Modes:
  - CTL_AUTH_MODE=disabled (default dev)
  - CTL_AUTH_MODE=azure_ad (validate Entra ID JWTs)
- Connectors read credentials from env or secret stores. For production, wire to Key Vault or managed identities.

---

## Connectors included (template)

- local: CSV/Parquet reader (fully functional)
- azure_sql: SQLAlchemy-based template (requires driver and connection string)
- mysql: SQLAlchemy-based template
- databricks: stub template for Databricks SQL endpoint or Unity Catalog via SQL connector

Add your own in `src/ctl_core/connectors/` and register them in `registry.py`.

---

## Transformations included (template)

- normalize (min-max)
- moving_average (simple rolling window)
- seasonal_adjustment (stub with optional statsmodels)

Add more in `src/ctl_core/transforms/` and register them.

---

## FAME-like query adapter (preview)

Basic adapter to translate a constrained, FAME-style request to CTL query parameters for backward compatibility (see `fame_syntax.py`). This is intentionally minimal—extend as required for your users.

---

## Security

- Dev mode skips auth for local productivity.
- Azure AD (Entra ID) mode validates Bearer tokens using tenant JWKS.
- Scopes and roles: Map app roles/scopes to CTL “operations” or “datasets” as you evolve governance.

See docs/20-security.md for details.

---

## Deployment

- Dockerfile for containerization.
- docker-compose for local.
- For Azure:
  - Container Apps or App Service for API
  - Entra ID app registration
  - Managed identity + Key Vault for secrets
  - Optional Azure API Management in front for throttling and observability

See docs/10-architecture.md and docs/50-onboarding.md.

---

## What’s missing / next steps to make this successful

- Data governance and lineage: Integrate with Databricks Unity Catalog, Purview/OpenLineage for lineage, and dataset certification labels.
- Observability: Centralized logging, tracing (OpenTelemetry), metrics (Prometheus), dashboards, and alerting SLOs/SLAs.
- Secrets and credentials: Use Key Vault or secret manager; phase out .env in prod.
- Role-based access (RBAC/ABAC): Fine-grained dataset access by role, group, geography; guardrails for PII.
- Schema contracts and data quality: Great Expectations/dbt tests; CI gates for transformations; user-facing data quality reports.
- Performance: Caching layer (Redis), async IO for APIs, vectorized transforms, and partition pushdown for large sources.
- Packaging for power users: 
  - Excel add-in (Office-js) or xlwings template with SSO,
  - R, Stata, MATLAB thin client packages published to internal registries.
- Cost control: Budgets and alerts; choose serverless/container autoscaling.
- Migration tooling: CSV-to-catalog publishing, FAME-to-CTL rule converter, and dependency mapping.
- Compliance: Data retention, audit logs, DPIA/records of processing, encryption posture.

A suggested roadmap is provided in docs/40-roadmap.md.

---

## Repository layout

- src/ctl_core: core package (connectors, transforms, registry, auth)
- src/ctl_api: FastAPI app
- src/ctl_cli: Typer CLI
- examples: simple clients (Python, R, Stata, MATLAB, Excel)
- docs: leadership and engineering docs
- tests: pytest suite
- .github/workflows: CI

MIT licensed. Contributions welcome.