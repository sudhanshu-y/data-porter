# be/models.py
from pydantic import BaseModel

class QueryResponse(BaseModel):
    delete_queries: list[str] = []
    insert_queries: list[list[str]] = []
