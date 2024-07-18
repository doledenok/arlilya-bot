"""Admin role realization."""

import sys
import os

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, constants
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

from start import start
from exam import Exam, ExamStatus
import exam_statistics


EXAMS_DATABASE_PATH = os.path.join(os.environ.get("TELEGRAM_ARLILYA_BOT_DATA", os.getcwd()), "exams_db.csv")
STATISTICS_DATABASE_PATH = os.path.join(os.environ.get("TELEGRAM_ARLILYA_BOT_DATA", os.getcwd()), "exams_stats_db.csv")

ADMIN_STATES_BASE = 10

(
    ADMIN_AWAITING_FOR_EXAM_REGISTRATION_FINISH,
    ADMIN_CREATE_EXAM,
    ADMIN_FINISH_EXAM_COMMAND,
    ADMIN_CHOOSING_STUDENT_FOR_EXAM_RESULTS_REVIEW,
    ADMIN_FINISH_EXAM_RESULTS_REVIEW,
) = range(ADMIN_STATES_BASE, ADMIN_STATES_BASE + 5)


async def admin_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    First function of admin role.

    It is called after user choose the creating exam scenario.
    """
    query = update.callback_query
    await query.answer()

    if query.data == "admin_start":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Итак, ваш сценарий — администратор экзамена"
        )
    else:
        await query.answer(f"Как вы это сделали? Бот сломан. Запрос {query.data} как callback выбора сценария")
        return await start(update, context)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Введите название нового экзамена:"
    )
    return ADMIN_CREATE_EXAM


async def admin_create_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exam_name = update.message.text
    if "exams" not in context.bot_data:
        context.bot_data["exams"] = {}
    exam = Exam(exam_name)
    context.bot_data["exams"][exam.id] = exam
    context.user_data["exam_id"] = exam.id
    context.user_data["exam"] = exam

    # TODO: убрать
    #context.bot_data["exams"][exam.id].add_speaker("Максим Доледенок")
    #context.bot_data["exams"][exam.id].add_speaker("Кто-то Кто-тович")
    #################

    return await admin_print_exam_registration_finish(update, context)


async def admin_print_exam_registration_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send invitation to exam admin to finish exam registration."""
    keyboard = [
        [
            InlineKeyboardButton(
                "Завершить регистрацию и\nпоказать\nсписок выступающих.", callback_data="admin_student_list"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Откройте список выступающих, когда будете готовы завершить регистрацию и приступить к экзамену:",
        reply_markup=reply_markup,
    )
    return ADMIN_AWAITING_FOR_EXAM_REGISTRATION_FINISH


async def admin_exam_registration_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Print list of registered students and send invitation to exam admin to finish exam."""
    query = update.callback_query
    await query.answer()

    if query.data != "admin_student_list":
        print(f'Strange query data {query.data} in admin_student_list', file=sys.stderr)
        return
    context.user_data["exam"].exam_status = ExamStatus.RegistrationFinished
    student_list_for_exam = context.bot_data["exams"][context.user_data["exam_id"]].get_speaker_names()
    if not student_list_for_exam:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ни одного выступающего не зарегистрировано! Пожалуйста, попробуйте позже."
        )
        return await admin_print_exam_registration_finish(update, context)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=", ".join(student_list_for_exam))

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Теперь вы можете послушать участников. Когда все участники закончат свои выступления, "
          "пожалуйста, отправьте команду /finish_exam"
    )
    return ADMIN_FINISH_EXAM_COMMAND


async def admin_finish_exam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save exam data and invite admin to look at them."""
    print("SDLKJFLKDSKJFKSDLKFJLSDKJFD\n\n\n\n")
    context.user_data["exam"].exam_status = ExamStatus.PresentationsFinished
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Ваш экзамен завершен. Теперь мы начинаем агрегировать результаты"
    )

    saved_rows = context.user_data["exam"].save_results(EXAMS_DATABASE_PATH)
    print(f'Processed and saved {saved_rows} rows for exam {context.user_data["exam_id"]}', file=sys.stdout)

    exam_statistics.calculate_exam_stats(context.user_data["exam_id"], EXAMS_DATABASE_PATH, STATISTICS_DATABASE_PATH)

    # Видимо, это лучше сделать через KeyboardMarkup, чтобы не спамить каждый раз таблицей-сообщением
    student_list_for_exam = context.user_data["exam"].get_speaker_names()
    number_of_students_on_exam = len(student_list_for_exam)
    N_COLS = 3
    N_ROWS = number_of_students_on_exam // N_COLS + int(number_of_students_on_exam % N_COLS != 0)
    students_results = [
        [
            f'{student_list_for_exam[i*N_COLS + j]}' if (i * N_COLS + j < number_of_students_on_exam) else ''
            for j in range(N_COLS)
        ]
        for i in range(N_ROWS)
    ]

    keyboard = []
    for i in range(N_ROWS):
        current_row = []
        for j in range(N_COLS):
            current_row.append(
                InlineKeyboardButton(students_results[i][j], callback_data=f"admin_student_{i*N_COLS + j}_results")
            )
        keyboard.append(current_row)
    keyboard.append(
        [InlineKeyboardButton("Здесь представлены результаты экзаменов для каждого выступающего:", callback_data="admin_all_students_results")]
    )
    keyboard.append(
        [InlineKeyboardButton("Завершить просмотр результатов", callback_data="admin_finish_review_results")]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здесь представлены результаты экзаменов для каждого выступающего:",
        reply_markup=reply_markup,
    )

    return ADMIN_CHOOSING_STUDENT_FOR_EXAM_RESULTS_REVIEW


async def admin_choosing_student_for_exam_results_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Invite admin to look students statistics."""
    query = update.callback_query
    await query.answer()

    if not query.data.endswith("_results"):
        print(f'Strange query data {query.data} in admin_exam_registration_finish', file=sys.stderr)
        return

    if query.data == 'admin_finish_review_results':
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Вы завершили экзамен.\nПоздравляем! До новых встреч!"
        )
        return await start(update, context)

    exam_id = context.user_data["exam_id"]
    students_names = context.user_data["exam"].get_speaker_names()
    if query.data == 'admin_all_students_results':
        exam_results = exam_statistics.get_exam_results(exam_id, students_names, STATISTICS_DATABASE_PATH)
        for student_id, student_result in exam_results.items():
            student_name = students_names[student_id]
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=f'{STATISTICS_DATABASE_PATH}_{exam_id}_{student_id}_results.png',
                caption=f"*{student_name}*\. Результаты\.\nЗамечания слушателей:\n```Замечания\n{student_result}\n```",
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )
    elif query.data.startswith("admin_student_"):
        student_id = int(query.data.split('_')[2])
        student_name = students_names[student_id]
        student_result = exam_statistics.get_student_results(
            exam_id, student_id, students_names, STATISTICS_DATABASE_PATH
        )

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=f'{STATISTICS_DATABASE_PATH}_{exam_id}_{student_id}_results.png',
            caption=f"*{student_name}*\. Результаты\.\nЗамечания слушателей:\n```Замечания\n{student_result}\n```",
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    else:
        print(f'Strange query data {query.data} in admin_exam_registration_finish', file=sys.stderr)

    # Видимо, это лучше сделать через KeyboardMarkup, чтобы не спамить каждый раз таблицей-сообщением
    student_list_for_exam = context.bot_data["exams"][context.user_data["exam_id"]].get_speaker_names()
    number_of_students_on_exam = len(student_list_for_exam)
    N_COLS = 3
    N_ROWS = number_of_students_on_exam // N_COLS + int(number_of_students_on_exam % N_COLS != 0)
    students_results = [
        [
            f'{student_list_for_exam[i*N_COLS + j]}' if (i * N_COLS + j < number_of_students_on_exam) else ''
            for j in range(N_COLS)
        ]
        for i in range(N_ROWS)
    ]

    keyboard = []
    for i in range(N_ROWS):
        current_row = []
        for j in range(N_COLS):
            current_row.append(
                InlineKeyboardButton(students_results[i][j], callback_data=f"admin_student_{i*N_COLS + j}_results")
            )
        keyboard.append(current_row)
    keyboard.append(
        [InlineKeyboardButton("Получить результаты для всех выступающих", callback_data="admin_all_students_results")]
    )
    keyboard.append(
        [InlineKeyboardButton("Завершить просмотр результатов", callback_data="admin_finish_review_results")]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здесь представлены результаты экзаменов для каждого выступающего:",
        reply_markup=reply_markup,
    )

    return ADMIN_CHOOSING_STUDENT_FOR_EXAM_RESULTS_REVIEW


admin_states = {
    ADMIN_AWAITING_FOR_EXAM_REGISTRATION_FINISH: [
        CallbackQueryHandler(admin_exam_registration_finish, pattern="^admin*"),
    ],
    ADMIN_CREATE_EXAM: [MessageHandler(filters.ALL, admin_create_exam)],
    ADMIN_FINISH_EXAM_COMMAND: [CommandHandler("finish_exam", admin_finish_exam_command)],
    ADMIN_CHOOSING_STUDENT_FOR_EXAM_RESULTS_REVIEW: [
        CallbackQueryHandler(admin_choosing_student_for_exam_results_button, pattern="^admin*"),
    ],
}
