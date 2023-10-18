from pydantic import BaseModel

class Tab(BaseModel):
    url: str
    source: str
