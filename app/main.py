from fastapi import FastAPI
from app.routers import cats
from app.routers import auth


app = FastAPI()

app.include_router(cats.router)
app.include_router(auth.router)

