from fastapi import FastAPI, HTTPException

from models import Tab, Bulk, BulkResponse
from consts import SOURCES
from sources import GPTSource, TabFetchingException

app = FastAPI()

gpt_source = GPTSource("https://guitarprotabs.net")

@app.get("/tabs/{source}/{query}")
async def get_tabs(source, query) -> list[Tab]:
    if (source not in SOURCES):
        raise HTTPException(status_code=400, detail=f"Invalid source. Supported sources: ")

    tabs = []
    if (source == "gpt" or source == "all"):
        try:
            tabs.append(Tab(url=gpt_source.fetch(query), source="gpt"))
        except TabFetchingException as e:
            raise HTTPException(status_code=404, detail=e.message)

    return tabs


@app.get("/bulk/{source}")
async def get_bulk_tabs(source, query_list: Bulk) -> BulkResponse:
    
    tabs = []
    errors = []
    for q in query_list.queries:
        try:
            tabs.append(Tab(url=gpt_source.fetch(q), source=source))
        except TabFetchingException as e:
            errors.append(q)

    return BulkResponse(tabs=tabs, errors=errors)
