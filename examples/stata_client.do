* Very simple Stata example using curl to call CTL API and import JSON via insheetjson (if installed).
local base "http://localhost:8000"

file open f using query.json, write replace
file write f `"{""connector"": ""local"", ""connector_config"": {""path"": ""data/example.csv""}, ""query"": {""select"": [""date"", ""series"", ""value""], ""where"": {""series"": ""GDP""}}}"'
file close f

!curl -s -X POST `"`base'/query"' -H "Content-Type: application/json" --data @query.json > out.json
type out.json
* If you have insheetjson: insheetjson using out.json