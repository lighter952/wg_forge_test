from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.database_func import get_user_from_bd

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#  TODO
#   Заменить функцию берущую пользователя напрямую из базы на работу с токеном
#


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # user = fake_decode_token(token)
    user = get_user_from_bd(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user