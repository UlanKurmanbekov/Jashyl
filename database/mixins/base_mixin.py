from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class BaseMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
