import re
from fastapi import HTTPException

class QueryValidator:
    @staticmethod
    def validate_select_query(select_query: str) -> None:
        """
        Validate the structure of a SELECT query to ensure it is well-formed and safe.
        """
        if not select_query.lower().startswith("select"):
            raise HTTPException(status_code=400, detail="Invalid query: must start with SELECT")

        if "from" not in select_query.lower():
            raise HTTPException(status_code=400, detail="Invalid query: missing FROM clause")

        # Check for unsafe patterns (e.g., UNION, DROP, TRUNCATE, DELETE)
        unsafe_patterns = [r"\bunion\b", r"\bdrop\b", r"\btruncate\b", r"\bdelete\b", r"\balter\b"]
        for pattern in unsafe_patterns:
            if re.search(pattern, select_query, re.IGNORECASE):
                raise HTTPException(status_code=400, detail="Invalid query: contains unsafe SQL patterns")

    @staticmethod
    def sanitize_where_clause(where_clause: str) -> str:
        """
        Sanitize the WHERE clause to prevent SQL injection.

        Allowed Characters:

        Alphanumeric Characters: 
        \w (letters and numbers)
        Whitespace: \s
        Common Operators: =, >, <
        Parentheses: ()
        Quotes: ' (single quote), " (double quote)

        Disallowed Characters:
        This includes special characters and SQL control characters like ;, --, etc.
        """
        # Allow only alphanumeric characters and common operators in the WHERE clause
        sanitized_clause = re.sub(r'[^\w\s=><\(\)\'"]', '', where_clause)
        return sanitized_clause

    @staticmethod
    def validate_query_for_sql_injection(query: str) -> None:
        """
        Validate any SQL query to ensure it does not contain forbidden SQL commands.
        """
        # List of forbidden SQL commands
        forbidden_commands = [
            r'\bunion\b',     # UNION command
            r'\bdrop\b',      # DROP command
            r'\btruncate\b',  # TRUNCATE command
            r'\bdelete\b',    # DELETE command
            r'\balter\b'      # ALTER command
        ]
        
        # Check for any forbidden commands
        for command in forbidden_commands:
            if re.search(command, query, re.IGNORECASE):
                raise HTTPException(status_code=400, detail=f"Invalid query: contains forbidden SQL command '{command.strip()}'")
        
        # Check for suspicious characters or patterns that may indicate injection attempts
        if re.search(r'--|;', query):
            raise HTTPException(status_code=400, detail="Invalid query: contains suspicious characters or potential SQL injection patterns")
