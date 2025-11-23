"""Tools registration."""

tools = [
    {
        "type": "function",
        "name": "run_query",
        "description": "Run a SQL query against a database and return the results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute.",
                },
            },
            "required": ["query"],
        },
    }
]
