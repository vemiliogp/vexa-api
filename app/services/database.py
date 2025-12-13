"""Database service module."""

from dataclasses import dataclass
from logging import error

from psycopg import connect


@dataclass
class DatabaseService:
    """Service to handle database operations."""

    def check_connection(self, connection_url: str) -> bool:
        """
        Check if the database connection is successful.
        """
        try:
            with connect(connection_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    return True
        except Exception as e:
            error(f"Database connection failed: {e}")
            return False
