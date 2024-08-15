from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class DateTimeMixin:
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
