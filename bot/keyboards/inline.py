from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Dict, Tuple


def get_inline_buttons(
        *,
        buttons: Dict[str, str],
        sizes: Tuple[int, ...] = (2,)
) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру с кнопками.

    Args:
        buttons (dict): Словарь с текстами кнопок в качестве ключей и значениями
                        URL или callback_data.
        sizes (tuple): Размеры строк клавиатуры, по умолчанию (2,).

    Returns:
        InlineKeyboardMarkup: Клавиатура для использования в сообщениях бота.
    """
    keyboard = InlineKeyboardBuilder()

    for text, value in buttons.items():
        button = InlineKeyboardButton(
            text=text,
            switch_inline_query_current_chat=value
        )
        keyboard.add(button)

    return keyboard.adjust(*sizes).as_markup()
