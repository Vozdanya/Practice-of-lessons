from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.services.auth import authservice

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = authservice.decode_token(token)
    user_id = payload.get("user_id")
    return user_id