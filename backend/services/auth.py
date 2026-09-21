import jwt
from fastapi import Header, HTTPException, status
from pydantic import BaseModel

from config import settings


class AuthenticatedUser(BaseModel):
    id: str


async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
) -> AuthenticatedUser:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
            options={"require": ["exp", "sub", "aud"]},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton d’authentification invalide.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton d’authentification invalide.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthenticatedUser(id=user_id)
