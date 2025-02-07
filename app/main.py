import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from configs.config import app_settings
from api.routers import router as v1_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_settings.SERVICE_NAME,
        version=app_settings.SERVICE_VERSION,
        docs_url="/docs/",
        openapi_url="/openapi.json/",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        v1_router, prefix=f"/api/{app_settings.API_VERSION}"
    )

    return app


app = create_app()

if __name__ == "__main__":
    host = "0.0.0.0"
    uvicorn.run(
        "main:app",
        host=host,
        port=app_settings.SERVICE_PORT,
        reload=True,
    )
