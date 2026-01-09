"""Tools registration."""

tools = [
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
            "name": "save_insight",
            "description": "Save an insight to the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the insight.",
                    },
                    "description": {
                        "type": "string",
                        "description": "The description of the insight.",
                    },
                },
                "required": ["title", "description"],
            },
        },
    },
]
