"""The FastAPI application.

    make run     # http://127.0.0.1:8000/docs
    make test

Everything the app can do lives under ``app/routes/``. Adding a feature means adding
a router there and including it below.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.model_client import ModelError
from app.routes import libraries, summary

app = FastAPI(
    title="Facilities API",
    version="1.0.0",
    description="A small records API with one model-backed endpoint, used as the "
                "starting point for the Week 5 specification exercise.",
)

# Order matters: `/libraries/summary` must be registered before `/libraries/{library_id}`,
# or the path-parameter route captures the literal path "summary" first.
app.include_router(summary.router)
app.include_router(libraries.router)


@app.exception_handler(ModelError)
async def model_error_handler(request: Request, exc: ModelError) -> JSONResponse:
    """Any model failure that escapes a route becomes a 503 rather than a 500.

    A route that wants different behaviour catches the exception itself — see
    :func:`app.routes.libraries.describe_library`.
    """
    return JSONResponse(status_code=503,
                        content={"detail": str(exc), "code": "model_unavailable"})


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok"}
