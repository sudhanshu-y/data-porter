from fastapi import FastAPI
from be.routes import query_generator

app = FastAPI()

# Include the query router
app.include_router(query_generator.router, prefix="/api/sql-generator", tags=["sql-generator"])

