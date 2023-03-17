from fastapi import APIRouter, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from home_task.exceptions import BackendException
from home_task.handlers import backend_exception_handler
from home_task.routers import home_task_router
from settings import Settings

app = FastAPI(
    debug=Settings.DEBUG,
    title="HRF_home_task",
    description="",
    version="0.0.1",
    openapi_url="/openapi.json" if Settings.ENABLE_OPENAPI else None,
    redoc_url=None,
    docs_url="/docs/" if Settings.ENABLE_OPENAPI else None,
    default_response_class=ORJSONResponse,
)

app.add_exception_handler(BackendException, backend_exception_handler)


app.add_middleware(middleware_class=GZipMiddleware, minimum_size=512)  # №3
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=Settings.CORS_ALLOW_ORIGINS,
    allow_credentials=Settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=Settings.CORS_ALLOW_METHODS,
    allow_headers=Settings.CORS_ALLOW_HEADERS,
)  # №2
app.add_middleware(middleware_class=ProxyHeadersMiddleware, trusted_hosts=Settings.TRUSTED_HOSTS)  # №1


api_router = APIRouter()


@api_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Health check.",
    description="Health check endpoint.",
)
async def healthcheck() -> ORJSONResponse:
    return ORJSONResponse(
        content={
            "status": "success",
            "data": None,
            "message": "Health check.",
            "code": status.HTTP_200_OK,
        },
        status_code=status.HTTP_200_OK,
    )


app.include_router(router=api_router)
app.include_router(router=home_task_router)


if __name__ == "__main__":  # pragma: no cover
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(
        app="main:app",
        host=Settings.HOST,
        port=Settings.PORT,
        loop="uvloop",
        reload=True,
        reload_delay=5,
        log_level=Settings.LOG_LEVEL,
        use_colors=Settings.LOG_USE_COLORS,
    )
