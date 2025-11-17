"""Middleware to require an handle sessions."""

from fastapi import HTTPException, Request, status


def require_active_session(request: Request):
    """Middleware to ensure an active session exists."""

    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión requerida"
        )
    return user
