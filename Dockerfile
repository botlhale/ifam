FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# System deps for pandas/pyodbc if you enable sql extras
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl gcc g++ unixodbc-dev \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY data /app/data

RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -e ".[stats]"  # base + stats example

ENV CTL_AUTH_MODE=disabled
EXPOSE 8000

CMD ["uvicorn", "ctl_api.main:app", "--host", "0.0.0.0", "--port", "8000"]