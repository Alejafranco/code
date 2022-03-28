import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from .config import secret_token
from .db import engine

bearer_scheme = HTTPBearer()


def authenticate_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    if not secrets.compare_digest(credentials.credentials, secret_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return credentials.credentials


def get_session():
    with Session(engine) as session:
        yield session
