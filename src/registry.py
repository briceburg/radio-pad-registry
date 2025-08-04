from fastapi import FastAPI
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from api.accounts import router as accounts_router
from api.players import router as players_router
from api.station_presets import router as station_presets_router


def create_app(in_unit_test=False):
    """Create FastAPI application."""
    app = FastAPI(
        title="RadioPad Registry API",
        version="0.0.0",
        docs_url="/v1/api-docs/",
        redoc_url="/v1/redoc/",
        openapi_url="/v1/openapi.json"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Root redirect to swagger docs
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/v1/api-docs/")

    # Health check endpoint
    @app.get("/healthz", include_in_schema=False)
    async def health():
        return PlainTextResponse("ok")

    # Include routers with v1 prefix
    app.include_router(accounts_router, prefix="/v1", tags=["Accounts"])
    app.include_router(players_router, prefix="/v1", tags=["Players"])
    app.include_router(station_presets_router, prefix="/v1", tags=["Station Presets"])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("registry:app", host="127.0.0.1", port=8080, reload=True)
