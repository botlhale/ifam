import requests

BASE = "http://localhost:8000"

print("Connectors:", requests.get(f"{BASE}/connectors").json())
print("Transforms:", requests.get(f"{BASE}/transforms").json())

# Query local file
q = {
    "connector": "local",
    "connector_config": {"path": "data/example.csv"},
    "query": {"select": ["date", "series", "value"], "where": {"series": "GDP"}}
}
resp = requests.post(f"{BASE}/query", json=q)
print("Query result:", resp.json())

# Pipeline
t = {
    "input": q,
    "pipeline": [
        {"name": "normalize", "params": {"columns": ["value"]}},
        {"name": "moving_average", "params": {"column": "value", "window": 2}}
    ]
}
resp = requests.post(f"{BASE}/transform", json=t)
print("Transform result:", resp.json())