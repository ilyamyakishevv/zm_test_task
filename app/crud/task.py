from typing import Type, TypeVar, List, Optional

from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.base import Base
from models.task import Task
from schemas.task import TaskCreateDB, TaskUpdateDB

ModelType = TypeVar("ModelType", bound=Base)


class CRUDTask:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
            self,
            db: AsyncSession,
            create_schema: TaskCreateDB     
            ) -> ModelType:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await db.execute(stmt)
        result = result.scalars().first()
        await db.commit()

        return result

    async def read_by_id(
            self,
            db: AsyncSession,
            obj_id: int
            ) -> Optional[List[ModelType]]:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(stmt)

        return result.scalars().first()

    async def update(
        self, db: AsyncSession, obj_id: int, update_schema: TaskUpdateDB
    ) -> Optional[ModelType]:
        obj = await self.read_by_id(db, obj_id)
        if obj:
            data = update_schema.model_dump(exclude_unset=True)
            stmt = (
                update(self.model)
                .where(self.model.id == obj_id)
                .values(**data)
                .returning(self.model)
            )
        result = await db.execute(stmt)
        result = result.scalars().first()
        await db.commit()
        await db.refresh(result)
        return result

    async def delete(
            self,
            db: AsyncSession,
            obj_id: int
            ) -> Optional[ModelType]:
        obj = await self.read_by_id(db, obj_id)
        if not obj:
            return None
        await db.delete(obj)
        await db.commit()
        return obj

    async def read_multi(self, db: AsyncSession) -> List[ModelType]:
        result = await db.execute(select(self.model))
        return result.scalars().unique().all()


crud_task = CRUDTask(Task)
