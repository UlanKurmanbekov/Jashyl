from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base
from database.mixins.base_mixin import BaseMixin
from database.mixins.user_mixin import UserRelationMixin


if TYPE_CHECKING:
    pass


class Pet(BaseMixin, UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = 'pet'

    name: Mapped[str] = mapped_column(String(32), default='Безымянный')
    level: Mapped[int] = mapped_column(Integer, default=0)
    state: Mapped[bool] = mapped_column(default=True)
    money: Mapped[int] = mapped_column(Integer, default=0)
    experience: Mapped[int] = mapped_column(Integer, default=0)
    max_experience: Mapped[int] = mapped_column(Integer, default=10)


