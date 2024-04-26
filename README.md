# Бот для оценки выступлений в центре "Арлилия"

Центр по избавлению от заикания "Арлилия":
https://www.arlilia.ru

Бот сделан на основе проекта для спецкурса "Совместная разработка приложений на Python" факультета ВМК МГУ:
https://github.com/doledenok/arlilya-bot

## Описание

Бот представляет собой систему опроса слушателей во время проведения выступлений в центре "Арлилия". Слушатели будут оценивать выступающих по различным критериям, отвечая на вопросы телеграм-бота.
Оценки собираются, и в конце экзамена выдается статистика, как общая, так и для всех выступащих по отдельности.

## Запуск

В проекте используется язык Python3.10.
Для запуска бота сначала установить необходимые пакеты, запустив команду:

``` bash
pip install Pipfile
```

Теперь можно запустить бота:

``` bash
doit start
```

## Реализация

Проект представляет собой телеграм-бота, написанного на языке Python с помощью библиотеки python-telegram-bot.

## Функционал

Приблизительный сценарий работы бота:

![Приблизительный сценарий работы бота](https://raw.githubusercontent.com/doledenok/arlilya-bot/main/docs/source/_static/scenario.jpg)

## Интерфейса

Бот имеет текстовый интерфейс и взаимодействует с пользователем через Telegram.

### Примеры интерфейса:

Стартовый выбор сценария:

![](https://raw.githubusercontent.com/doledenok/arlilya-bot/main/docs/source/_static/start.jpg)
-----

Организатор. Проведение экзамена

![](https://raw.githubusercontent.com/doledenok/arlilya-bot/main/docs/source/_static/exam_managing.jpg)
----

Организатор. Просмотр результатов экзамена

![](https://raw.githubusercontent.com/doledenok/arlilya-bot/main/docs/source/_static/review_exam_results.jpg)
----

Выступающий. Регистрация на экзамен

![](https://raw.githubusercontent.com/doledenok/arlilya-bot/main/docs/source/_static/user_exam_joining.jpg)
----

Выступающий. Оценка выступающих

![](https://raw.githubusercontent.com/doledenok/arlilya-bot/main/docs/source/_static/user_rating.jpg)
