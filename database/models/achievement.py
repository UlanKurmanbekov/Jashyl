from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base
from database.mixins.intidpk_mixin import IntIdPKMixin
from database.mixins.date_time_mixin import DateTimeMixin


class AchievementType(IntIdPKMixin, DateTimeMixin, Base):
    name: Mapped[str] = mapped_column()
    achievements: Mapped[list['Achievement']] = relationship(back_populates='achievement_type')


class Achievement(IntIdPKMixin, DateTimeMixin, Base):
    description: Mapped[str]
    achievement_type_id: Mapped[int] = mapped_column(ForeignKey('achievement_types.id'))
    achievement_type: Mapped['AchievementType'] = relationship(back_populates='achievements')
