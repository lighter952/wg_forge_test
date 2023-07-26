from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from app.models import Cat
from app.database_func import get_cats_from_db, append_new_cat_to_db, is_offset_in_range

app = FastAPI(title="My cats!")


@app.get("/")
async def index():
    return RedirectResponse(url='/ping')


@app.get("/ping")
async def ping():
    return {"Cats Service. Version 0.1"}


@app.get("/cats/")
async def cats(attribute: str = 'name', order: str = 'asc', offset: int = 0, limit: int = 100):
    if order not in ['desc', 'asc']:
        raise HTTPException(status_code=422, detail="Order can be desc or asc only!")
    if attribute not in ['name', 'color', 'tail_length', 'whiskers_length']:
        raise HTTPException (status_code=422, detail="Unknown attribute!")
    if is_offset_in_range(offset) is False:
        offset = 0
    if limit < 0:
        limit = 100
    return JSONResponse(get_cats_from_db(attribute, order, offset, limit))


@app.post("/cat")
async def create_cat(cat: Cat):

    append_new_cat_to_db(cat)
    return {"message": "Cat created successfully"}