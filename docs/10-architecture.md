# Architecture

- CTL Core Library
  - Connectors: local files (CSV/Parquet), Azure SQL, MySQL, Databricks (template).
  - Transformations: normalize, moving average, seasonal adjustment (STL).
  - Registries: discoverable connectors/transforms; add new types with minimal code.
  - FAME-like adapter: translate legacy queries to QuerySpec.
- CTL API (FastAPI)
  - Endpoints: /health, /connectors, /transforms, /query, /transform, /fame/query
  - Output formats: JSON (extendable to CSV/Parquet/Excel export).
  - Auth: Disabled (dev) or Entra ID JWT validation (prod).
- Clients
  - Python, R, Stata, MATLAB examples.
  - Excel via xlwings (template script).
- Deployments
  - Local: uvicorn or docker-compose.
  - Cloud: Azure App Service/Container Apps, with Key Vault for secrets.
  - Add Azure API Management in front for throttling and centralized auth if desired.

Sequence (from diagram):
1. Users authenticate with Entra ID (prod).
2. Tools call CTL REST API.
3. CTL API invokes CTL Core: connectors fetch data.
4. Transformations are applied via pipeline.
5. Results returned to tools (JSON/CSV/Excel).
6. Optionally, IFAM/IME adapter can call CTL similarly (company-specific).

Extension points:
- New connectors: implement query() and register in registry.
- New transforms: implement apply() and register.
- Policies: add middleware for dataset-level authorization.