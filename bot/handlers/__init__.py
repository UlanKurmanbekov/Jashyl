__all__ = ('router',)

from aiogram import Router
from .pet_actions import router as pet_router
from .inline_handlers import router as inline_router

router = Router()

router.include_routers(
    pet_router,
    inline_router
)
