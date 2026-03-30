"""Tool to describe the structure of database tables."""

from logging import error

from app.utils.connection_url import normalize_connection_url
from psycopg import connect


def describe_table(connection_url: str, table_name: str) -> list:
    """Describe the structure of a database table."""

    query = """
        SELECT
            cols.column_name,
            cols.data_type,
            cols.is_nullable,
            cols.column_default,
            pgd.description AS comment
        FROM information_schema.columns AS cols
        LEFT JOIN pg_catalog.pg_class AS c
            ON c.relname = cols.table_name
        LEFT JOIN pg_catalog.pg_namespace AS n
            ON n.oid = c.relnamespace
        LEFT JOIN pg_catalog.pg_description AS pgd
            ON pgd.objoid = c.oid
           AND pgd.objsubid = cols.ordinal_position
        WHERE cols.table_name = %s
        ORDER BY cols.ordinal_position;
    """

    try:
        with connect(normalize_connection_url(connection_url)) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (table_name,))
                return cur.fetchall()
    except Exception as e:
        error(f"Database query failed: {e}")
        return []
