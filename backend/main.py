import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from database import init_db, UPLOADS_DIR
from routers import api

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
INGRESS_PATH = os.environ.get("INGRESS_PATH", "")

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
    _index_html = None

    def _get_index_html():
        global _index_html
        if _index_html is None:
            with open(os.path.join(STATIC_DIR, "index.html")) as f:
                _index_html = f.read()
            # Rewrite asset paths to be under the ingress path
            if INGRESS_PATH:
                _index_html = _index_html.replace('./assets/', f'{INGRESS_PATH}/assets/')
        return _index_html

    @app.get("/")
    async def serve_index():
        return HTMLResponse(_get_index_html())

    @app.get("/{full_path:path}")
    async def serve_static_or_fallback(full_path: str):
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return HTMLResponse(_get_index_html())
