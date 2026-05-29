from fastapi import FastAPI

from app.core.config import settings

from app.api.routes.health import router as health_router
from app.api.routes.upload import router as upload_router
from app.api.routes.extract import router as extract_router
from app.api.routes.embed import router as embed_router
from app.api.routes.search import router as search_router
from app.api.routes.chat import router as chat_router
from app.api.routes.summary import router as summary_router
from app.api.routes.stream_chat import (
    router as stream_chat_router
)
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.multi_chat import (
    router as multi_chat_router
)
from app.api.routes.multi_graph import (
    router as graph_router
)





app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    graph_router,
    prefix=settings.API_V1_STR,
    tags=["Knowledge Graph"]
)

app.include_router(
    stream_chat_router,
    prefix=settings.API_V1_STR,
    tags=["Streaming Chat"]
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
    multi_chat_router,
    prefix=settings.API_V1_STR,
    tags=["Multi PDF Chat"]
)

app.include_router(
    summary_router,
    prefix=settings.API_V1_STR,
    tags=["Summary"]
)

app.include_router(
    search_router,
    prefix=settings.API_V1_STR,
    tags=["Search"]
)

app.include_router(
    chat_router,
    prefix=settings.API_V1_STR,
    tags=["Chat"]
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to PaperMind API"
    }