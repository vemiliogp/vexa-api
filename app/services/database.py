"""Database service module."""

from dataclasses import dataclass
from logging import error, info
from typing import List, Optional

from app.utils.connection_url import normalize_connection_url
from psycopg import connect


@dataclass
class DatabaseService:
    """Service to handle database operations."""

    @staticmethod
    def get_tables(connection_url: str) -> Optional[List[str]]:
        """
        Retrieve all table names from the database.
        """
        try:
            with connect(normalize_connection_url(connection_url)) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_type = 'BASE TABLE'
                        ORDER BY table_name;
                    """
                    )
                    tables = [row[0] for row in cur.fetchall()]
                    info(f"Retrieved {len(tables)} tables from database")
                    return tables
        except Exception as e:
            error(f"Failed to retrieve tables: {e}")
            return None

    @staticmethod
    def get_tables_with_columns(connection_url: str) -> Optional[List[str]]:
        """
        Retrieve table names with their columns in the format: table (col1, col2, ...).
        """
        try:
            with connect(normalize_connection_url(connection_url)) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT t.table_name, c.column_name
                        FROM information_schema.tables t
                        JOIN information_schema.columns c
                            ON t.table_name = c.table_name
                            AND t.table_schema = c.table_schema
                        WHERE t.table_schema = 'public'
                        AND t.table_type = 'BASE TABLE'
                        ORDER BY t.table_name, c.ordinal_position;
                    """
                    )
                    rows = cur.fetchall()
                    tables: dict = {}
                    for table_name, column_name in rows:
                        tables.setdefault(table_name, []).append(column_name)
                    result = [
                        f"{table} ({', '.join(cols)})" for table, cols in tables.items()
                    ]
                    info(f"Retrieved {len(result)} tables with columns from database")
                    return result
        except Exception as e:
            error(f"Failed to retrieve tables with columns: {e}")
            return None

    def check_connection(self, connection_url: str) -> bool:
        """
        Check if the database connection is successful.
        """
        try:
            with connect(normalize_connection_url(connection_url)) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    return True
        except Exception as e:
            error(f"Database connection failed: {e}")
            return False
