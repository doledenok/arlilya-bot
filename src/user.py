"""User role realization."""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    filters,
    MessageHandler,
)

from exam import Exam, ExamStatus
from start import start


"""
В context.bot_data["exams"] находятся объекты класса exam.Exam, где хранится вся информация об экзаменах
В context.user_data есть ключи:
 - exam_id - id экзамена для текущего пользователя
 - exam - объект класса exam.Exam
 - name - имя пользователя
 - user_id - id пользователя
 - speaker_id - id выступающего, которого сейчас оценивает пользователь
"""


USER_STATES_BASE = 100

(
    USER_MAIN,
    USER_WAIT_CREATING_EXAM,
    USER_CHOOSE_EXAM,
    USER_NAME,
    USER_SHOW_LIST_OF_SPEAKERS,
    USER_STORE_SPEAKER_ID,
    USER_SHOW_CRITERIA,
    USER_CHOOSE_RATE,
    USER_RATE_STUTTER_COUNT_STORE,
    USER_RATE_CALMNESS_STORY_STORE,
    USER_RATE_CALMNESS_QUESTIONS_STORE,
    USER_RATE_EYE_CONTACT_STORY_STORE,
    USER_RATE_EYE_CONTACT_QUESTIONS_STORE,
    USER_RATE_ANSWERS_SKILL_STORE,
    USER_RATE_NOTES_STORE,
) = range(USER_STATES_BASE, USER_STATES_BASE + 15)


async def user_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    First function of user role.

    It is called after user choose the joining exam scenario.
    """
    query = update.callback_query

    if query.data == "user_start":
        await query.answer()

        # TODO: убрать при релизе
        """
        if "exams" not in context.bot_data:
            context.bot_data["exams"] = {}
        exam = Exam("Тестовый экзамен")
        context.bot_data["exams"][exam.id] = exam
        context.bot_data["exams"][exam.id].add_speaker("Максим Доледенок")
        context.bot_data["exams"][exam.id].add_speaker("Кто-то Кто-тович")
        """
        #################

        if "exams" not in context.bot_data:
            return await user_wait_creating_exams(update, context)
        return await user_show_list_of_exams(update, context)
    await query.answer(f"Как вы это сделали? Бот сломан. Запрос {query.data} как callback выбора сценария")
    return await start(update, context)


async def user_wait_creating_exams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()
    if "exams" not in context.bot_data:
        keyboard = [[InlineKeyboardButton("Попробовать ещё раз", callback_data=f"user_no_exams")]]
        await context.bot.send_message(
            update.effective_chat.id,
            "Не найдено запущенных экзаменов. Подождите, пока админ создает экзамен.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return USER_WAIT_CREATING_EXAM
    else:
        return await user_show_list_of_exams(update, context)


async def user_show_list_of_exams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #await context.bot.send_message(update.effective_chat.id, "Пожалуйста, выберите экзамен, к которому вы хотите присоединиться:")
    keyboard = []
    for exam in context.bot_data["exams"].values():
        keyboard.append([InlineKeyboardButton(exam.name, callback_data=f"user_exam{exam.id}")])

    await context.bot.send_message(
        update.effective_chat.id,
        text="Пожалуйста, выберите экзамен, к которому вы хотите присоединиться:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return USER_CHOOSE_EXAM


async def user_choose_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process user choise of exam to join existed exam."""
    query = update.callback_query
    exam_id = query.data[9:]
    await query.answer()
    if not exam_id.isdigit():
        await context.bot.send_message(update.effective_chat.id, f"Как вы это сделали? Бот сломан. Запрос {query.data} как callback выбора экзамена.")
        return await user_show_list_of_exams(update, context)

    exam_id = int(exam_id)
    if "exams" not in context.bot_data or exam_id not in context.bot_data["exams"]:
        await context.bot.send_message(update.effective_chat.id, f"Как вы это сделали? Бот сломан. Запрос {query.data} как callback выбора экзамена, такой id экзамена не найден.")
        return USER_CHOOSE_EXAM
    context.user_data["exam_id"] = exam_id
    context.user_data["exam"] = context.bot_data["exams"][exam_id]
    await context.bot.send_message(update.effective_chat.id, "Успешно! Вы подключены к экзамену")
    await context.bot.send_message(update.effective_chat.id, "Пожалуйста, введите ваши имя и фамилию:")
    return USER_NAME


async def user_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add user name to the list of speakers. And invite user to start listening."""
    name = update.message.text
    context.user_data["name"] = name
    user_id = context.user_data["exam"].add_speaker(name)
    if user_id is None:
        await context.bot.send_message(update.effective_chat.id, "Это имя уже существует! Пожалуйста, введите другое имя.")
        return USER_NAME
    context.user_data["user_id"] = user_id
    keyboard = [[InlineKeyboardButton("Начать прослушивание", callback_data="user_start_listening")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Здравствуйте, {name}!\nДавайте подождем, пока создатель экзамена завершит регистрацию, "
          "и начнем прослушивание наших докладчиков.", reply_markup=reply_markup)
    return USER_SHOW_LIST_OF_SPEAKERS


async def user_show_list_of_speakers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """If exam is started - then print speakers list and invite user to rate them."""
    query = update.callback_query
    await query.answer()

    while context.user_data["exam"].exam_status != ExamStatus.RegistrationFinished:
        keyboard = [
            [InlineKeyboardButton("Начать прослушивание", callback_data="user_start_listening")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            update.effective_chat.id,
            text="Извините, создатель экзамена еще не завершил регистрацию. Попробуйте немного позже.",
            reply_markup=reply_markup,
        )
        return USER_SHOW_LIST_OF_SPEAKERS

    speakers = context.user_data["exam"].get_speaker_names(context.user_data["user_id"])
    keyboard = [
        [
            InlineKeyboardButton(f"{speakers[j]}", callback_data=f"user_speaker{j}")
            for j in range(i, min(len(speakers), i + 2))
        ]
        for i in range(0, len(speakers), 2)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        update.effective_chat.id, "Вот список выступающих. Выберите, кого вы хотите оценить:", reply_markup=reply_markup
    )
    return USER_STORE_SPEAKER_ID


async def user_store_speaker_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store speaker that user want to rate now and show the criteria of rating."""
    query = update.callback_query
    await query.answer()

    if query.data.startswith("user_speaker"):
        speaker_id = int(query.data[len("user_speaker"):])
        context.user_data["speaker_id"] = speaker_id
    else:
        await query.answer(f"Как вы это сделали? Бот сломан. Запрос {query.data} как callback для выбора выступающего.")
        return USER_SHOW_LIST_OF_SPEAKERS

    await context.bot.send_message(
        update.effective_chat.id,
        f"Выбран выступающий {context.user_data['exam'].get_name_by_id(speaker_id)}",
    )
    return await user_show_criteria(update, context)

def form_rate_presence(context: ContextTypes.DEFAULT_TYPE, criteria: str) -> str:
    if context.user_data["exam"].check_rate(context.user_data["user_id"], context.user_data["speaker_id"], criteria):
        return "✅ "
    return ""

async def user_show_criteria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the criteria of rating."""
    keyboard = [
        [InlineKeyboardButton(f"{form_rate_presence(context, 'stutter_count')}Количество спазматических задержек", callback_data="user_rate_stutter_count")],
        [InlineKeyboardButton(f"{form_rate_presence(context, 'calmness_story')}Внутреннее спокойствие на подготовленной речи", callback_data="user_rate_calmness_story")],
        [InlineKeyboardButton(f"{form_rate_presence(context, 'calmness_questions')}Внутреннее спокойствие на спонтанной речи", callback_data="user_rate_calmness_questions")],
        [InlineKeyboardButton(f"{form_rate_presence(context, 'eye_contact_story')}Зрительный контакт на подготовленной речи", callback_data="user_rate_eye_contact_story")],
        [InlineKeyboardButton(f"{form_rate_presence(context, 'eye_contact_quesitons')}Зрительный контакт на спонтанной речи", callback_data="user_rate_eye_contact_questions")],
        [InlineKeyboardButton(f"{form_rate_presence(context, 'answer_skill')}Умение отвечать на вопросы", callback_data="user_rate_answers_skill")],
        [InlineKeyboardButton(f"{form_rate_presence(context, 'notes')}Замечания и впечатления про экзамен", callback_data="user_rate_notes")],
        [InlineKeyboardButton(f"<< Выбрать другого выступающего", callback_data="user_speakers")],
        [InlineKeyboardButton(f"❌ Завершить участие в экзамене", callback_data="user_finish_exam")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        update.effective_chat.id, "Выберите, что вы хотите оценить:", reply_markup=reply_markup
    )
    return USER_CHOOSE_RATE


async def user_get_one_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Support function for getting number between 0 and 10."""
    answer = update.message.text
    if not answer.isdigit():
        await context.bot.send_message(update.effective_chat.id, "Пожалуйста, введите число!")
        return None
    score = int(answer)
    if not 0 <= score <= 10:
        await context.bot.send_message(update.effective_chat.id, "Пожалуйста, введите число от 1 до 10!")
        return None
    return score


async def user_rate_stutter_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, "Введите количество")
    return USER_RATE_STUTTER_COUNT_STORE


async def user_rate_stutter_count_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text
    if not answer.isdigit():
        await context.bot.send_message(update.effective_chat.id, "Пожалуйста, введите число!")
        return await user_show_criteria(update, context)
    score = int(answer)
    context.user_data["exam"].add_answer(
        context.user_data["user_id"], context.user_data["speaker_id"], "stutter_count", score
    )
    await context.bot.send_message(update.effective_chat.id, "Спасибо! Сохранено.")
    return await user_show_criteria(update, context)


async def user_rate_calmness_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rate calmness while telling the story."""
    await context.bot.send_message(update.effective_chat.id, "Введите число от 0 до 10, где 10 - отлично")
    return USER_RATE_CALMNESS_STORY_STORE


async def user_rate_calmness_story_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the score of calmness while telling the story."""
    score = await user_get_one_number(update, context)
    if score is None:
        return await user_show_criteria(update, context)
    context.user_data["exam"].add_answer(
        context.user_data["user_id"], context.user_data["speaker_id"], "calmness_story", score
    )
    await context.bot.send_message(update.effective_chat.id, "Спасибо! Сохранено.")
    return await user_show_criteria(update, context)


async def user_rate_calmness_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rate calmness while answering the questions."""
    await context.bot.send_message(update.effective_chat.id, "Введите число от 0 до 10, где 10 - отлично")
    return USER_RATE_CALMNESS_QUESTIONS_STORE


async def user_rate_calmness_questions_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the score of calmness while answering the questions."""
    score = await user_get_one_number(update, context)
    if score is None:
        return await user_show_criteria(update, context)
    context.user_data["exam"].add_answer(
        context.user_data["user_id"], context.user_data["speaker_id"], "calmness_questions", score
    )
    await context.bot.send_message(update.effective_chat.id, "Спасибо! Сохранено.")
    return await user_show_criteria(update, context)


async def user_rate_eye_contact_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rate eye contact while telling the story."""
    await context.bot.send_message(update.effective_chat.id, "Введите число от 0 до 10, где 10 - отлично")
    return USER_RATE_EYE_CONTACT_STORY_STORE


async def user_rate_eye_contact_story_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the score of eye contact while telling the story."""
    score = await user_get_one_number(update, context)
    if score is None:
        return await user_show_criteria(update, context)
    context.user_data["exam"].add_answer(
        context.user_data["user_id"], context.user_data["speaker_id"], "eye_contact_story", score
    )
    await context.bot.send_message(update.effective_chat.id, "Спасибо! Сохранено.")
    return await user_show_criteria(update, context)


async def user_rate_eye_contact_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rate eye contact while answering the questions."""
    await context.bot.send_message(update.effective_chat.id, "Введите число от 0 до 10, где 10 - отлично")
    return USER_RATE_EYE_CONTACT_QUESTIONS_STORE


async def user_rate_eye_contact_questions_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the score of eye contact while answering the questions."""
    score = await user_get_one_number(update, context)
    if score is None:
        return await user_show_criteria(update, context)
    context.user_data["exam"].add_answer(
        context.user_data["user_id"], context.user_data["speaker_id"], "eye_contact_quesitons", score
    )
    await context.bot.send_message(update.effective_chat.id, "Спасибо! Сохранено.")
    return await user_show_criteria(update, context)


async def user_rate_answers_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rate skill of answering questions."""
    await context.bot.send_message(update.effective_chat.id, "Введите число от 0 до 10, где 10 - отлично")
    return USER_RATE_ANSWERS_SKILL_STORE


async def user_rate_answers_skill_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the score of skill of answering questions."""
    score = await user_get_one_number(update, context)
    if score is None:
        return await user_show_criteria(update, context)
    context.user_data["exam"].add_answer(
        context.user_data["user_id"], context.user_data["speaker_id"], "answer_skill", score
    )
    await context.bot.send_message(update.effective_chat.id, "Спасибо! Сохранено.")
    return await user_show_criteria(update, context)


async def user_rate_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add some notes about speaker performance."""
    await context.bot.send_message(update.effective_chat.id, "Введите заметки, которые вы хотите сохранить:")
    return USER_RATE_NOTES_STORE


async def user_rate_notes_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store some notes about speaker performance."""
    context.user_data["exam"].add_answer(
        context.user_data["user_id"], context.user_data["speaker_id"], "notes", update.message.text
    )
    await context.bot.send_message(update.effective_chat.id, "Спасибо! Сохранено.")
    return await user_show_criteria(update, context)


async def user_finish_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finish exam and print the start menu."""
    await context.bot.send_message(update.effective_chat.id, "Спасибо за участие в экзамене!\nТеперь вы можете дождаться окончания экзамена, чтобы увидеть "
          "общие и индивидуальные результаты.\nУдачи!")
    return await start(update, context)


user_states = {
    USER_MAIN: [MessageHandler(filters.ALL, user_main)],
    USER_CHOOSE_EXAM: [CallbackQueryHandler(user_choose_exam, pattern="^user_exam*")],
    USER_WAIT_CREATING_EXAM: [CallbackQueryHandler(user_wait_creating_exams, pattern="^user_no_exams")],
    USER_NAME: [MessageHandler(filters.ALL, user_name)],
    USER_SHOW_LIST_OF_SPEAKERS: [CallbackQueryHandler(user_show_list_of_speakers, pattern="^user_start_listening$")],
    USER_STORE_SPEAKER_ID: [CallbackQueryHandler(user_store_speaker_id, pattern="^user_speaker*")],
    USER_SHOW_CRITERIA: [MessageHandler(filters.ALL, user_show_criteria)],
    USER_CHOOSE_RATE: [
        CallbackQueryHandler(user_rate_stutter_count, pattern="^user_rate_stutter_count$"),
        CallbackQueryHandler(user_rate_calmness_story, pattern="^user_rate_calmness_story$"),
        CallbackQueryHandler(user_rate_calmness_questions, pattern="^user_rate_calmness_questions$"),
        CallbackQueryHandler(user_rate_eye_contact_story, pattern="^user_rate_eye_contact_story$"),
        CallbackQueryHandler(user_rate_eye_contact_questions, pattern="^user_rate_eye_contact_questions$"),
        CallbackQueryHandler(user_rate_answers_skill, pattern="^user_rate_answers_skill$"),
        CallbackQueryHandler(user_rate_notes, pattern="^user_rate_notes$"),
        CallbackQueryHandler(user_show_list_of_speakers, pattern="^user_speakers$"),
        CallbackQueryHandler(user_finish_exam, pattern="^user_finish_exam$"),
    ],
    USER_RATE_STUTTER_COUNT_STORE: [MessageHandler(filters.ALL, user_rate_stutter_count_store)],
    USER_RATE_CALMNESS_STORY_STORE: [MessageHandler(filters.ALL, user_rate_calmness_story_store)],
    USER_RATE_CALMNESS_QUESTIONS_STORE: [MessageHandler(filters.ALL, user_rate_calmness_questions_store)],
    USER_RATE_EYE_CONTACT_STORY_STORE: [MessageHandler(filters.ALL, user_rate_eye_contact_story_store)],
    USER_RATE_EYE_CONTACT_QUESTIONS_STORE: [MessageHandler(filters.ALL, user_rate_eye_contact_questions_store)],
    USER_RATE_ANSWERS_SKILL_STORE: [MessageHandler(filters.ALL, user_rate_answers_skill_store)],
    USER_RATE_NOTES_STORE: [MessageHandler(filters.ALL, user_rate_notes_store)],
}
