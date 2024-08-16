from sqlalchemy import Table, insert, text
from sqlalchemy.dialects import oracle
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from be.database import engine, metadata
from be.validators.query_validator import QueryValidator

# Utility function to extract the table name from the SELECT query
def extract_table_name(select_query: str) -> str:
    QueryValidator.validate_select_query(select_query)  # Validate the query
    parts = select_query.lower().split("from")
    from_parts = parts[1].split()
    return from_parts[0].strip()

# Service function to generate a DELETE SQL statements
def generate_delete_statements(select_queries: list[str]) -> list[str]:
    delete_statements = []
    for select_query in select_queries:
        table_name = extract_table_name(select_query)

        # Extract and sanitize the WHERE clause
        where_clause = select_query.split("where", 1)[1] if "where" in select_query.lower() else ""
        sanitized_where_clause = QueryValidator.sanitize_where_clause(where_clause)

        delete_statements.append(f"DELETE FROM {table_name} WHERE {sanitized_where_clause}")

    return delete_statements


# Service function to generate INSERT SQL statements
def generate_insert_statements(select_queries: list[str]) -> list[list[str]]:
    all_insert_statements = []

    for select_query in select_queries:
        table_name = extract_table_name(select_query)
        table = Table(table_name, metadata, autoload_with=engine)

        insert_statements = []
        try:
            with engine.connect() as connection:
                result = connection.execute(text(select_query))
                rows = result.fetchall()

                if rows:
                    for row in rows:
                        insert_stmt = insert(table).values(**row)
                        compiled = insert_stmt.compile(dialect=oracle.dialect(), compile_kwargs={"literal_binds": True})
                        insert_statements.append(str(compiled))

            all_insert_statements.append(insert_statements)
        
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database operation failed")

    return all_insert_statements

