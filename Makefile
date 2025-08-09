.PHONY: run test lint format

run:
\tuvicorn ctl_api.main:app --reload --host 0.0.0.0 --port 8000

test:
\tpytest -q

lint:
\truff check src tests

format:
\truff format src tests