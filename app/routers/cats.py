from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from app.utils.dependencies import get_current_user
from app.schemas.users import User
from app.schemas.cats import Cat
from app.models.database_func import get_cats_from_db, append_new_cat_to_db, is_offset_in_range, get_user_from_bd

router = APIRouter()


def get_user(username: str) -> dict:
    return get_user_from_bd(username)


def fake_decode_token(token):
    user = get_user(token)
    return user


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


@router.get("/cats", tags=["Cats"])
async def cats(cats_from_bd: list[dict] = Depends(validate_params), current_user: User = Depends(get_current_user)):
    return JSONResponse(cats_from_bd, status_code=200)


@router.post("/cat", tags=["Cats"])
async def create_cat(cat: Cat, current_user: User = Depends(get_current_user)):
    append_new_cat_to_db(cat)
    return JSONResponse({"message": "Cat created successfully"}, status_code=201)
