from pydantic import BaseModel

from typing import List

class Tab(BaseModel):
    url: str
    source: str

class Bulk(BaseModel):
    queries: List[str]

class BulkResponse(BaseModel):
    tabs: List[Tab]
    errors: List[str]
