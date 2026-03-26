"""Utilities for database connection URLs."""

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def normalize_connection_url(url: str) -> str:
    """Add sslmode=require to remote connection URLs that don't already specify it."""
    parsed = urlparse(url)
    local_hosts = {"localhost", "127.0.0.1", "::1"}
    if parsed.hostname in local_hosts:
        return url

    params = parse_qs(parsed.query, keep_blank_values=True)
    if "sslmode" not in params:
        params["sslmode"] = ["require"]

    new_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=new_query))
