from fastapi import FastAPI

from app.core.config import settings

from app.api.routes.health import router as health_router
from app.api.routes.upload import router as upload_router
from app.api.routes.extract import router as extract_router
from app.api.routes.embed import router as embed_router
from app.api.routes.search import router as search_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG
)


app.include_router(
    health_router,
    prefix=settings.API_V1_STR,
    tags=["Health"]
)

app.include_router(
    upload_router,
    prefix=settings.API_V1_STR,
    tags=["Upload"]
)

app.include_router(
    extract_router,
    prefix=settings.API_V1_STR,
    tags=["Extract"]
)

app.include_router(
    embed_router,
    prefix=settings.API_V1_STR,
    tags=["Embeddings"]
)

app.include_router(
    search_router,
    prefix=settings.API_V1_STR,
    tags=["Search"]
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to PaperMind API"
    }