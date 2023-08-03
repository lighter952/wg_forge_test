from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from passlib.context import CryptContext
from app.schemas.users import User, UserInDB
from app.schemas.cats import Cat
from app.database_func import get_cats_from_db, append_new_cat_to_db, is_offset_in_range, get_user_from_bd, get_user_hash
import time
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Summary


app = FastAPI()
myctx: CryptContext = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])
Instrumentator().instrument(app).expose(app)
request_duration_histogram = Summary('http_request_duration_seconds', 'Request duration in seconds')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user1(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def get_user(username: str) -> dict:
    return get_user_from_bd(username)


def fake_decode_token(token):
    user = get_user(token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.get('disabled'):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", tags=["Login"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    start_time = time.time()

    user = get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not myctx.verify(form_data.password, get_user_hash(user.get('user_id'))):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    time_taken = time.time() - start_time
    request_duration_histogram.observe(time_taken)
    return {"access_token": user.get('username'), "token_type": "bearer"}


@app.get("/users/me", tags=["Login"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


def validate_params(attribute: str = 'name', order: str = 'asc', offset: int = 0, limit: int = 100) -> list[dict]:
    if order not in ['desc', 'asc']:
        raise HTTPException(status_code=422, detail="Order can be desc or asc only!")
    if attribute not in ['name', 'color', 'tail_length', 'whiskers_length']:
        raise HTTPException (status_code=422, detail="Unknown attribute!")
    if is_offset_in_range(offset) is False:
        offset = 0
    if limit < 0:
        limit = 100
    return get_cats_from_db(attribute, order, offset, limit)


@app.get("/cats/", tags=["Cats"])
async def cats(cats_from_bd: list[dict] = Depends(validate_params), current_user: User = Depends(get_current_user)):

    return JSONResponse(cats_from_bd)


@app.post("/cat", tags=["Cats"])
async def create_cat(cat: Cat, current_user = Depends(get_current_user)):
    append_new_cat_to_db(cat)
    return {"message": "Cat created successfully"}