from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Dict, Tuple


def get_inline_buttons(
        *,
        buttons: Dict[str, str],
        sizes: Tuple[int, ...] = (2,),
        switch_inline: bool = False,
        callback_inline: bool = False
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for text, value in buttons.items():
        if switch_inline:
            button = InlineKeyboardButton(
                text=text,
                switch_inline_query_current_chat=value
            )
        elif callback_inline:
            button = InlineKeyboardButton(
                text=text,
                callback_data=value
            )
        else:
            raise ValueError("Выберите либо `switch_inline`, либо `callback_inline`")

        keyboard.add(button)

    return keyboard.adjust(*sizes).as_markup()
