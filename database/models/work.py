from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base
from database.mixins.intidpk_mixin import IntIdPKMixin
from database.mixins.date_time_mixin import DateTimeMixin


if TYPE_CHECKING:
    from database.models.pet import Pet


class WorkType(IntIdPKMixin, DateTimeMixin, Base):
    name: Mapped[str] = mapped_column(String(32))

    work: Mapped[list['Work']] = relationship(back_populates='work_type')


class Work(IntIdPKMixin, DateTimeMixin, Base):
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(Text)
    min_reward: Mapped[int] = mapped_column(Integer, default=0)
    max_reward: Mapped[int] = mapped_column(Integer, default=250)
    chance_no_reward: Mapped[int] = mapped_column(Integer, default=0)
    chance_injury: Mapped[int] = mapped_column(Integer, default=0)

    work_type_id: Mapped[int] = mapped_column(ForeignKey('work_types.id'))
    work_type: Mapped['WorkType'] = relationship(back_populates='work')
    work_times: Mapped[list['PetWorkTime']] = relationship(back_populates='work')


class PetWorkTime(IntIdPKMixin, Base):
    telegram_id: Mapped[int] = mapped_column(ForeignKey('pets.telegram_id'), unique=True)
    work_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    next_work_time: Mapped[DateTime] = mapped_column(DateTime)
    work_id: Mapped[int] = mapped_column(ForeignKey('works.id'), nullable=True)

    pet: Mapped['Pet'] = relationship(back_populates='work_time')
    work: Mapped['Work'] = relationship(back_populates='work_times')
