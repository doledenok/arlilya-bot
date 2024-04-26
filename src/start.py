"""The start of conversation without separation on roles."""

import sys

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

import messages

# First state after start
CHOOSING_ROLE = 0
#CHOOSING_LANGUAGE = 1



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command.

    Print the start menu with role choice - admin or user.
    """

    keyboard = [
        [
            InlineKeyboardButton("Создать экзамен", callback_data="admin_start"),
        ],
        [
            InlineKeyboardButton("Присоединиться к экзамену", callback_data="user_start"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        update.effective_chat.id, "Пожалуйста, выберите сценарий:", reply_markup=reply_markup
    )
    return CHOOSING_ROLE

    """
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="interface_language_en"),
            InlineKeyboardButton("Русский", callback_data="interface_language_ru"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        update.effective_chat.id, "Choose interface language / Выберите язык интерфейса:", reply_markup=reply_markup
    )
    return CHOOSING_LANGUAGE
    """


async def choosing_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Invite user to choose the interface language - english or russian.

    WARNING!!! Not using for now. Currently support only russian language.
    """
    query = update.callback_query
    await query.answer()

    if not query.data.startswith("interface_language_"):
        print(f'Strange query data {query.data} in admin_main', file=sys.stderr)
        return

    user_language = query.data[-2:]
    if user_language not in ["en", "ru"]:
        print(f'Strange query data {query.data} in admin_main', file=sys.stderr)
        return

    context.user_data["user_language"] = user_language

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=messages.USER_LANGUAGE[user_language] % user_language
    )

    keyboard = [
        [
            InlineKeyboardButton(messages.CREATE_EXAM[user_language], callback_data="admin_start"),
            InlineKeyboardButton(messages.JOIN_EXAM[user_language], callback_data="user_start"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        update.effective_chat.id, messages.CHOOSE_SCENARIO[user_language], reply_markup=reply_markup
    )
    return CHOOSING_ROLE
