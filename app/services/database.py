"""Database service module."""

from dataclasses import dataclass
from logging import error, info
from typing import List, Optional

from psycopg import connect

from app.utils.connection_url import normalize_connection_url


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
