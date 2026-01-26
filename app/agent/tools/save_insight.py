"""Tool to run SQL queries against a database."""

from logging import error
from os import getenv

from psycopg import connect


def save_insight(
    connection_id: int, user_id: str, title: str, description: str,
) -> list:
    """Run a SQL query against the database."""
    connection_url = getenv("DATABASE_URL")

    try:
        with connect(connection_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO insight (user_id, title, description, connection_id) VALUES (%s, %s, %s, %s) RETURNING id;",
                    (user_id, title, description, connection_id),
                )
                rows = cur.fetchall()

                return [[str(val) for val in row] for row in rows]
    except Exception as e:
        error(f"Database query failed: {e}")
        return []
