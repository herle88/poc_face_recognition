import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from database import init_db, UPLOADS_DIR
from routers import api

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

os.makedirs(UPLOADS_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Face Recognition POC", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
app.include_router(api.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}


# Serve built frontend if it exists (production / add-on mode)
if os.path.isdir(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(request: Request, full_path: str):
        # Serve index.html for all non-API, non-asset routes (SPA fallback)
        index = os.path.join(STATIC_DIR, "index.html")
        return FileResponse(index)
