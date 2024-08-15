from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base
from database.mixins.intidpk_mixin import IntIdPKMixin
from database.mixins.date_time_mixin import DateTimeMixin
from utils.random_image import get_random_image

if TYPE_CHECKING:
    pass


class Pet(IntIdPKMixin, DateTimeMixin, Base):

    name: Mapped[str] = mapped_column(String(32), default='Безымянный')
    image: Mapped[str] = mapped_column(String(255), default=get_random_image)
    level: Mapped[int] = mapped_column(Integer, default=0)
    state: Mapped[bool] = mapped_column(default=True)
    money: Mapped[int] = mapped_column(Integer, default=0)
    experience: Mapped[int] = mapped_column(Integer, default=0)
    max_experience: Mapped[int] = mapped_column(Integer, default=10)
    telegram_id: Mapped[int] = mapped_column(BigInteger)


