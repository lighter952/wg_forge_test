from app.schemas.users import User, PasswordChange
from app.models.database_func import get_user_from_bd, get_user_hash, update_password_hash
from app.utils.dependencies import get_current_user
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from passlib.context import CryptContext


router = APIRouter()
myctx: CryptContext = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


def fake_decode_token(token):
    user = get_user_from_bd(token)
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.get('disabled'):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/")
async def index():
    return RedirectResponse('/users/me')


@router.post("/token", tags=["Login"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_from_bd(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not myctx.verify(form_data.password, get_user_hash(user.get('user_id'))):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": user.get('username'), "token_type": "bearer"}


@router.get("/users/me", tags=["Login"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/update_password", tags=["Login"])
def change_password(form_data: PasswordChange):
    user = get_user_from_bd(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not myctx.verify(form_data.old_password, get_user_hash(user.get('user_id'))):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    update_password_hash(user.get('user_id'), str(myctx.hash(form_data.new_password)))
    return {"Password for user {} was changed!".format(form_data.username)}


