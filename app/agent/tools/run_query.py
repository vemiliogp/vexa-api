"""Tool to run SQL queries against a database."""

from logging import error

from psycopg import connect


def run_query(connection_url: str, query: str) -> list:
    """Run a SQL query against the database."""

    try:
        with connect(connection_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
    except Exception as e:
        error(f"Database query failed: {e}")
        return []
