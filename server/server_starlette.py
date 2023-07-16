from starlette.applications import Starlette
from starlette.responses import JSONResponse,RedirectResponse
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from app import get_cats_from_db

async def ping(request):
    return PlainTextResponse("Cats Service. Version 0.1")

async def cats(request):
    return JSONResponse(get_cats_from_db())

async def index(request):
    return RedirectResponse(url="/ping")

app = Starlette(debug=True, routes=[
    Route('/ping', ping),
    Route('/cats', cats),
    Route('/', index)
])