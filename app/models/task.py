from datetime import datetime

from sqlalchemy import DateTime, func, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_info: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
        )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
        )
    datetime_to_do: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return f"Task {self.id}"
    