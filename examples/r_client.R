library(httr)
library(jsonlite)

base <- "http://localhost:8000"

q <- list(
  connector="local",
  connector_config=list(path="data/example.csv"),
  query=list(select=list("date","series","value"), where=list(series="GDP"))
)

resp <- POST(paste0(base, "/query"),
             body=toJSON(q, auto_unbox=TRUE),
             encode="json")
print(content(resp, "parsed"))