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
    },
    {
        "type": "function",
        "name": "describe_table",
        "description": "Describe the schema of a database table.",
        "parameters": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "The name of the table to describe.",
                },
            },
            "required": ["table_name"],
        },
    },
]
