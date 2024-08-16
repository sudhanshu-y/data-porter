# be/routes/query_generator.py

from fastapi import APIRouter, HTTPException
from be.models import QueryResponse
from be.services.query_service import generate_delete_statements, generate_insert_statements

router = APIRouter()

@router.post("/delete", response_model=QueryResponse)
async def generate_delete_queries(select_queries: list[str]):
    try:
        delete_statements = generate_delete_statements(select_queries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return QueryResponse(delete_queries=delete_statements, insert_queries=[])

@router.post("/insert", response_model=QueryResponse)
async def generate_insert_queries(select_queries: list[str]):
    try:
        insert_statements = generate_insert_statements(select_queries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return QueryResponse(delete_queries=[], insert_queries=insert_statements)

@router.post("/delete-insert", response_model=QueryResponse)
async def generate_both_queries(select_queries: list[str]):
    try:
        delete_statements = generate_delete_statements(select_queries)
        insert_statements = generate_insert_statements(select_queries)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return QueryResponse(
        delete_queries=delete_statements,
        insert_queries=insert_statements
    )
