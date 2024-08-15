from typing import TYPE_CHECKING
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base
from database.mixins.base_mixin import BaseMixin

if TYPE_CHECKING:
    from database.models.pet import Pet


class User(BaseMixin, Base):
    first_name: Mapped[str]
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger(), unique=True)

    pet: Mapped['Pet'] = relationship(uselist=False, back_populates='user')
