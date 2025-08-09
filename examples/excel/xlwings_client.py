import xlwings as xw
import requests

BASE = "http://localhost:8000"

def ctl_fetch(series="GDP"):
    q = {
        "connector": "local",
        "connector_config": {"path": "data/example.csv"},
        "query": {"select": ["date", "series", "value"], "where": {"series": series}}
    }
    resp = requests.post(f"{BASE}/query", json=q)
    resp.raise_for_status()
    return resp.json()

def main():
    wb = xw.Book.caller()
    sht = wb.sheets[0]
    data = ctl_fetch(sht.range("B1").value or "GDP")
    # write header
    headers = list(data[0].keys()) if data else ["date","series","value"]
    sht.range("A3").value = [headers] + [list(r.values()) for r in data]

if __name__ == "__main__":
    xw.serve()