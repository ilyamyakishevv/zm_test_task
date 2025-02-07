from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.database import get_async_db
from crud.task import crud_task
from models.task import Task
from schemas.task import TaskResponse, TaskCreate, TaskUpdate

router = APIRouter()

@router.get("/tasks/list/", response_model=List[TaskResponse])
async def get_tasks(
    db: AsyncSession = Depends(get_async_db)
):
    return await crud_task.read_multi(db)

@router.post(
        "/tasks/create/",
        response_model=TaskResponse, 
        status_code=status.HTTP_201_CREATED,
             )
async def create_task(
    create_data: TaskCreate,
    db: AsyncSession = Depends(get_async_db)
):
    new_task = await crud_task.create(db, create_data)
    return new_task

@router.get("/tasks/{task_id}/", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    task = await crud_task.read_by_id(db, obj_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id {task_id} not found"
        )
    return task

@router.patch(
        "/tasks/{task_id}/update/",
        response_model=TaskResponse,
        status_code=status.HTTP_200_OK
        )
async def update_task(
    task_id: int,
    update_data: TaskUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    task = await crud_task.read_by_id(db, obj_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id {task_id} not found"
        )
    
    updated_task = await crud_task.update(
        db,
        obj_id=task.id,
        update_schema=update_data
        )

    return await crud_task.read_by_id(db=db, obj_id=updated_task.id)

@router.delete(
        "/tasks/{task_id}/delete/",
        status_code=status.HTTP_204_NO_CONTENT
            )
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    task = await crud_task.read_by_id(db, obj_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id {task_id} not found"
        )
    return await crud_task.delete(db, obj_id=task_id)
