"""
Messages from telegram bot on english and russian for localization.

WARNING!!! Currently support only russian language.
"""


USER_LANGUAGE = {"en": "Your language is %s.", "ru": "Вы выбрали язык %s."}
CREATE_EXAM = {"en": "Create exam", "ru": "Создать экзамен"}
JOIN_EXAM = {"en": "Join exam", "ru": "Присоединиться к экзамену"}
CHOOSE_SCENARIO = {"en": "Please choose the scenario:", "ru": "Пожалуйста, выберите сценарий:"}


EXAM_ID_ENTERING = {
    "en": "Please enter exam id. Creator of exam should tell it to you:",
    "ru": "Пожалуйста, введите идентификатор экзамена. Создатель экзамена должен сообщить вам об этом:",
}
INCONSISTENCY_MESSAGE = {
    "en": "How have you done it? Bot is inconsistent.",
    "ru": "Как вы это сделали? Бот работает непоследовательно.",
}
EXAM_ID_ENTERING_NOT_NUMBER_ERROR = {
    "en": "Please enter the number -- exam id:",
    "ru": "Пожалуйста, введите число -- идентификатор экзамена:",
}
EXAM_ID_ENTERING_NO_EXAMS_ERROR = {
    "en": "The is no registrated exams. Wait for exam creation",
    "ru": "Экзамены не зарегистрированы. Дождитесь создания экзамена",
}
EXAM_ID_ENTERING_NOT_REGISTRATED_ERROR = {
    "en": "Exam %d is not registered. Please enter the existed exam id:",
    "ru": "Экзамен %d не зарегистрирован. Пожалуйста, введите идентификатор существующего экзамена:",
}
EXAM_ID_ENTERING_SUCCESS = {"en": "Success! You are connected to the exam", "ru": "Успешно! Вы подключены к экзамену"}
NAME_ENTERING = {"en": "Please enter your name and surname:", "ru": "Пожалуйста, введите ваши имя и фамилию:"}
NAME_ENTERING_COLLISION_ERROR = {
    "en": "This name already exists! Enter another please",
    "ru": "Это имя уже существует! Введите другое, пожалуйста",
}
START_LISTENING = {"en": "Start listening", "ru": "Начните прослушивание"}
GREETING_MESSAGE = {
    "en": "Hello %s!\nLet's wait till exam creator finishes the registration and start our speakers listening.",
    "ru": "Здравствуйте, %s!\nДавайте подождем, пока создатель экзамена завершит регистрацию,"
          "и начнем прослушивание наших докладчиков.",
}
EXAM_REGISTRATION_NOT_FINISHED = {
    "en": "Sorry, exam creator has not finished exam registration yet. Check it again a bit later.",
    "ru": "Извините, создатель экзамена еще не завершил регистрацию на экзамен. Проверьте это еще раз чуть позже.",
}
SPEAKERS_LIST_TO_RATE = {
    "en": "Here is the list of speakers. Choose who you want to rate:",
    "ru": "Вот список выступающих. Выберите, кого вы хотите оценить:",
}
SPEAKER_TO_RATE_CHOICE = {"en": "You chose %s", "ru": "Оцениваемый студент --- %s"}
CALMNESS_STORY = {"en": "Calmness while telling a story", "ru": "Спокойствие при рассказе истории"}
CALMNESS_QUESTIONS = {"en": "Calmness while answering questions", "ru": "Спокойствие при ответе на вопросы"}
EYE_STORY = {"en": "Eye contact while telling a story", "ru": "Зрительный контакт при рассказе истории"}
EYE_QUESTIONS = {"en": "Eye contact while answering questions", "ru": "Зрительный контакт при ответе на вопросы"}
ANSWER_SKILL = {"en": "The skill to answer questions", "ru": "Умение отвечать на вопросы"}
NOTES_OF_LISTENER = {"en": "Notes about performance", "ru": "Замечания о выступлении"}
CHOOSE_ANOTHER_SPEAKER = {"en": "Choose another speaker", "ru": "Выберите другого докладчика"}
FINISH_RATING = {"en": "Finish rating", "ru": "Завершить оценивание"}
CHOOSE_FIELD_TO_RATE = {"en": "Choose what do you want to rate:", "ru": "Выберите, что вы хотите оценить:"}
RATE_ENTERING_NOT_NUMBER_ERROR = {"en": "Please enter the number!", "ru": "Пожалуйста, введите номер!"}
RATE_ENTERING_RANGE_ERROR = {
    "en": "Please enter the number between 0 and 10!",
    "ru": "Пожалуйста, введите число от 0 до 10!",
}
RATE_ENTERING_DESCRIPTION = {
    "en": "Input number from 0 to 10 where 10 is excellent",
    "ru": "Введите число от 0 до 10, где 10 - отлично",
}
RATE_ENTERING_THANKS = {"en": "Thanks! Stored.", "ru": "Спасибо! Сохранено."}
NOTES_OF_LISTENER_ENTERING = {
    "en": "Enter notes you want to save:",
    "ru": "Введите заметки, которые вы хотите сохранить:",
}
RATE_PARTICIPATION_THANKS = {
    "en": "Thank you for participating in the exam!\nNow you can wait for exam finish to see the global "
          "and individual results.\nGood luck!",
    "ru": "Спасибо за участие в экзамене!\nТеперь вы можете дождаться окончания экзамена, чтобы увидеть "
          "общие и индивидуальные результаты.\nУдачи!",
}


ADMIN_SCENARIO_INFORM = {"en": "So your scenario is admin", "ru": "Итак, ваш сценарий - администратор экзамена"}
EXAM_ID_CREATION = {"en": "Your exam id is %d", "ru": "Ваш идентификатор экзамена - %d"}
EXAM_REGISTRATION_FINISH_PLUS_STUDENTS_LIST = {
    "en": "Finish registration and show students list",
    "ru": "Завершить регистрацию и показать список студентов.",
}
EXAM_REGISTRATION_FINISHING_DESCRIPTION = {
    "en": "Open students list when you are ready to finish registration and to start exam:",
    "ru": "Откройте список студентов, когда будете готовы завершить регистрацию и приступить к экзамену:",
}
EXAM_REGISTRATION_FINISHING_NO_STUDENTS_ERROR = {
    "en": "No registered student! Please try later.",
    "ru": "Ни одного студента не зарегистрировано! Пожалуйста, попробуйте позже",
}
EXAM_STARTING_PLUS_EXAM_FINISH_COMMAND = {
    "en": "Now you can listen to your students. When all your students finish their presentations, "
          "please, send command /finish_exam",
    "ru": "Теперь вы можете послушать своих студентов. Когда все ваши студенты закончат свои презентации, "
          "пожалуйста, отправьте команду /finish_exam",
}
EXAM_FINISH_PLUS_RESULTS_AGGREGATION = {
    "en": "Your exam is finished. Now we start to aggregate all results",
    "ru": "Ваш экзамен завершен. Теперь мы начинаем агрегировать результаты",
}
EXAM_ALL_RESULTS = {"en": "Get results for all students", "ru": "Получить результаты для всех студентов"}
EXAM_FINISH_REVIEW = {"en": "Finish results review", "ru": "Завершить просмотр результатов"}
EXAM_PER_STUDENT_RESULTS = {
    "en": "Your per-student exam results are here:",
    "ru": "Здесь представлены результаты экзаменов для каждого студента:",
}
EXAM_FINISH_REVIEW_DESCRIPTION = {
    "en": "You've clicked finish-button.\nCongratulations! See you soon!",
    "ru": "Вы завершили экзамен.\nПоздравляем! До новых встреч!",
}
EXAM_INDIVIDUAL_RESULTS = {
    "en": "*%s* results\.\nListeners notes:\n```Notes\n%s\n```",
    "ru": "*%s*\. Результаты\.\nЗамечания слушателей:\n```Замечания\n%s\n```",
}
