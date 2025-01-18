"""The script file that runs the telegram arlilya bot."""

import os
import sys

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler

from start import start, CHOOSING_ROLE
from admin import admin_main, admin_states, admin_finish_exam_command
from user import user_main, user_states


def main():
    """
    Configure and run telegram bot.
    
    It should be run from the root directory (arlilya-bot).
    """
    if not (token := os.environ.get("TELEGRAM_ARLILYA_BOT_TOKEN")):
        print("Can't find telegram token! Please set TELEGRAM_ARLILYA_BOT_TOKEN environment variable.")
        sys.exit(1)

    application = ApplicationBuilder().token(token).build()

    states = {
        #CHOOSING_LANGUAGE: [
        #    CallbackQueryHandler(choosing_language, pattern="^interface_language"),
        #],
        CHOOSING_ROLE: [
            CallbackQueryHandler(admin_main, pattern="^admin_start"),
            CallbackQueryHandler(user_main, pattern="^user_start"),
        ],
    }
    states |= admin_states | user_states

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("finish_exam", admin_finish_exam_command)],
        states=states,
        fallbacks=[CommandHandler("start", start), CommandHandler("finish_exam", admin_finish_exam_command)],
        # per_message=True,  # не очень ясно, что оно делает
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
