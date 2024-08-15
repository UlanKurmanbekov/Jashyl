from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base
from database.mixins.base_mixin import BaseMixin


class AchievementType(BaseMixin, Base):
    name: Mapped[str] = mapped_column()
    achievements: Mapped[list['Achievement']] = relationship(back_populates='achievement_type')


class Achievement(BaseMixin, Base):
    description: Mapped[str]
    achievement_type_id: Mapped[int] = mapped_column(ForeignKey('achievement_types.id'))
    achievement_type: Mapped['AchievementType'] = relationship(back_populates='achievements')
