"""Tool to run SQL queries against a database."""

from logging import error

from psycopg import connect

from app.utils.connection_url import normalize_connection_url


def run_query(connection_url: str, query: str) -> list:
    """Run a SQL query against the database."""

    try:
        with connect(normalize_connection_url(connection_url)) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

                return [[str(val) for val in row] for row in rows]
    except Exception as e:
        error(f"Database query failed: {e}")
        return []
