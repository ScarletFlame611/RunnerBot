# Telegram-бот для беговых тренировок @airunnerbot

## Описание
Это Telegram-бот, созданный для управления беговыми тренировками. Он имеет следующие функции:
- Регистрация пользователей.
- Отправка напоминаний о тренировках с возможностью включения и отключения.
- Работа с данными о тренировках, включая запись тренировок, вывод последних тренировок, сравнение результатов, статистику за год.
- Достижения за выполненные тренировки.
- Общение с виртуальным тренером
- Сбор отзывов от пользователей.

---

## Установка локально

### 1. Склонируйте репозиторий
```bash
git clone <URL-репозитория>
cd <название-папки>
```

### 2. Установите зависимости
```bash
pip install -r requirements.txt
```
### 3. Введите токены
В файле bot/utils/config.py введите токен для бота и ключ для GigaChat
```bash
BOT_TOKEN = ваш_токен
GigaChatKey = ваш_ключ
```
### 4. Запустите бота
```bash
python bot/main.py
```

## Запуск в телеграмм
Перейдите в  @airunnerbot. Пройдите регистрацию, набрав команду /start.
Доступные команды:
- **/start** - Начало работы и регистрация  
- **/help** - Помощь  
- **/menu** - Вывод меню  
- **/choose_menu** - Выбор уровня и цели  
- **/profile** - Просмотр своего профиля  
- **/choose_menu** - Изменение цели и уровня физической подготовки  
- **/add_run** - Добавление беговой тренировки  
- **/last_trainings** - Просмотр ваших последних тренировок  
- **/compare_two** - Сравнение двух последних тренировок  
- **/year_stats** - Просмотр вашей годовой статистики  
- **/achievements_info** - Просмотр информации о достижениях  
- **/my_achievements** - Просмотр своих достижений  
- **/ask_ai {текст}** - Общение с виртуальным тренером  
- **/advice** - Получение совета от виртуального тренера в зависимости от вашего уровня подготовки и цели  
- **/motivation** - Получение мотивационного сообщения от виртуального тренера в зависимости от вашего уровня подготовки и цели  
- **/enable_reminders** - Включение напоминаний  
- **/disable_reminders** - Выключение напоминаний  
- **/feedback** - Оставить отзыв  
