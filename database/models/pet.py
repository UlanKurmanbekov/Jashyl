from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    health: Mapped[int] = mapped_column(Integer, default=100)
    renamed: Mapped[str] = mapped_column(default=False)

    feed_time: Mapped['PetFeedTime'] = relationship('PetFeedTime', back_populates='pet', uselist=False)
    work_time: Mapped['PetWorkTime'] = relationship('PetWorkTime', back_populates='pet', uselist=False)


class PetFeedTime(IntIdPKMixin, Base):
    telegram_id: Mapped[int] = mapped_column(ForeignKey('pets.telegram_id'), unique=True)
    feed_time: Mapped[DateTime] = mapped_column(DateTime)
    next_feed_time: Mapped[DateTime] = mapped_column(DateTime)

    pet: Mapped["Pet"] = relationship('Pet', back_populates='feed_time')


class PetWorkTime(IntIdPKMixin, Base):
    telegram_id: Mapped[int] = mapped_column(ForeignKey('pets.telegram_id'), unique=True)
    work_time: Mapped[DateTime] = mapped_column(DateTime)
    next_work_time: Mapped[DateTime] = mapped_column(DateTime)

    pet: Mapped["Pet"] = relationship('Pet', back_populates='work_time')
