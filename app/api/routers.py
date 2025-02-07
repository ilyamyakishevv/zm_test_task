from fastapi import APIRouter

from .endpoints import router as task_router

router = APIRouter()

router.include_router(
    task_router,
    tags=["Task"],
)
