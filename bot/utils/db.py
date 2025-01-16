import sqlite3
from datetime import datetime, timedelta

DB_PATH = "../data/database.db"


def init_db():
    """Инициализация базы данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            age INTEGER,
            height REAL,
            weight REAL,
            level TEXT,  -- Уровень физической подготовки
            goal TEXT    -- Цель пользователя
        )
    """)

    # Создание таблицы тренировок
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            distance REAL,
            duration TEXT,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    # Создание таблицы достижений
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,         -- Название достижения
            description TEXT          -- Описание достижения
        )
    """)

    # Проверка и заполнение достижений
    achievements = [
        ("Первый шаг", "Завершить первую пробежку."),
        ("Марафонец", "Пробежать суммарно 42.2 км."),
        ("Часовой бегун", "Завершить тренировку длительностью более 1 часа."),
        ("Спортивная десятка", "Пробежать 10 км за одну тренировку."),
        ("Первая пятёрка", "Завершить 5 тренировок."),
        ("Первый десяток", "Завершить 10 тренировок."),
        ("Три в одном", "Пробежать трижды в один день."),
        ("Рекордсмен ленивых", "Завершить пробежку длиной меньше 1 км."),
    ]

    # Проверка, что таблица пуста
    cursor.execute("SELECT COUNT(*) FROM achievements")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO achievements (name, description)
            VALUES (?, ?)
        """, achievements)
        print("Таблица 'achievements' успешно заполнена.")
    else:
        print("Таблица 'achievements' уже содержит данные.")

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_achievements (
                user_id INTEGER,
                achievement_id INTEGER,
                date_awarded TEXT,          -- Дата получения достижения
                PRIMARY KEY (user_id, achievement_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (achievement_id) REFERENCES achievements (id)
            )
        """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS user_settings (
    user_id INTEGER,
    reminders_enabled BOOLEAN DEFAULT FALSE
    );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()


def is_user_registered(user_id: int) -> bool:
    """Проверяет, зарегистрирован ли пользователь."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)


def register_user(user_id: int, full_name: str, age: int, height: float, weight: float):
    """Регистрирует пользователя."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, full_name, age, height, weight, level, goal)
        VALUES (?, ?, ?, ?, ?, NULL, NULL)
    """, (user_id, full_name, age, height, weight))
    conn.commit()
    conn.close()


def update_user_field(user_id: int, field: str, value: str):
    """Обновляет указанное поле пользователя."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()


def log_run(user_id: int, distance: float, duration: str, date: str):
    """Добавляет запись о пробежке в базу данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO runs (user_id, distance, duration, date)
        VALUES (?, ?, ?, ?)
    """, (user_id, distance, duration, date))
    conn.commit()
    conn.close()


def get_user_runs(user_id: int):
    """Возвращает все пробежки пользователя."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT distance, duration, date
        FROM runs
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    runs = cursor.fetchall()
    conn.close()
    return runs


def get_user_profile(user_id: int):
    """Получает информацию о пользователе."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Получаем основную информацию о пользователе
    cursor.execute("""
        SELECT full_name, age, height, weight, level, goal
        FROM users WHERE user_id = ?
    """, (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        conn.close()
        return None

    # Получаем статистику по пробежкам
    cursor.execute("""
        SELECT COUNT(*), SUM(distance), GROUP_CONCAT(duration)
        FROM runs WHERE user_id = ?
    """, (user_id,))
    run_stats = cursor.fetchone()
    conn.close()

    total_duration_seconds = 0

    # Проверяем и обрабатываем данные о продолжительности пробежек
    if run_stats[2]:
        durations = run_stats[2].split(",")
        for duration in durations:
            try:
                hours, minutes, seconds = map(int, duration.split(":"))
                total_duration_seconds += hours * 3600 + minutes * 60 + seconds
            except ValueError:
                # Пропускаем некорректные записи
                continue

    # Конвертируем общее время в формат ЧЧ:ММ:СС
    hours, remainder = divmod(total_duration_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    total_duration = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    # Возвращаем результат
    return {
        "full_name": user_data[0],
        "age": user_data[1],
        "height": user_data[2],
        "weight": user_data[3],
        "level": user_data[4] or "Не указан",
        "goal": user_data[5] or "Не указана",
        "total_runs": run_stats[0] or 0,
        "total_distance": run_stats[1] or 0.0,
        "total_duration": total_duration,
    }


def get_last_trainings(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT distance, duration, date
        FROM runs
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 5
    """, (user_id,))
    last_trainings = cursor.fetchall()
    conn.close()
    return last_trainings


def get_last_two_trainings(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT distance, duration, date
        FROM runs
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 2
    """, (user_id,))
    last_two_trainings = cursor.fetchall()
    conn.close()
    return last_two_trainings


def get_trainings_last_year(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Текущая дата и дата год назад
    one_year_ago = (datetime.now() - timedelta(days=365)).date()
    cursor.execute("""
        SELECT distance, duration, date
        FROM runs
        WHERE user_id = ? AND date >= ?
        ORDER BY date ASC
    """, (user_id, one_year_ago))
    trainings = cursor.fetchall()
    conn.close()
    return trainings


def update_profile_in_db(user_id, field, value):
    # Подключаемся к базе данных
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Формируем запрос для обновления данных в таблице users
    query = f"UPDATE users SET {field} = ? WHERE user_id = ?"

    try:
        # Выполняем запрос
        cursor.execute(query, (value, user_id))
        conn.commit()  # Сохраняем изменения в базе данных

        print(f"Пользователь {user_id} обновил поле {field} на {value}")
    except Exception as e:
        print(f"Ошибка при обновлении данных: {e}")
    finally:
        # Закрываем соединение с базой данных
        conn.close()


def add_achievement(user_id: int, achievement_name: str):
    """Добавляет достижение пользователю."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Получаем ID достижения по его имени
    cursor.execute("SELECT id FROM achievements WHERE name = ?", (achievement_name,))
    achievement_id = cursor.fetchone()

    if achievement_id:
        achievement_id = achievement_id[0]

        # Вставляем в таблицу user_achievements, если такого достижения нет
        cursor.execute("""
            INSERT OR IGNORE INTO user_achievements (user_id, achievement_id, date_awarded)
            VALUES (?, ?, ?)
        """, (user_id, achievement_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    else:
        print(f"Достижение с названием '{achievement_name}' не найдено в базе данных.")

    conn.close()


def get_user_achievements(user_id: int):
    """Получает все достижения пользователя с датой получения."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.name, ua.date_awarded
        FROM achievements a
        JOIN user_achievements ua ON a.id = ua.achievement_id
        WHERE ua.user_id = ?
    """, (user_id,))

    achievements = cursor.fetchall()
    conn.close()
    return achievements


def get_user_settings(user_id):
    """
    Получить настройки пользователя.
    :param user_id: ID пользователя.
    :return: Словарь с настройками пользователя.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT reminders_enabled FROM user_settings WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {"reminders_enabled": bool(result[0])}
    else:
        # Если пользователь отсутствует, возвращаем настройки по умолчанию
        return {"reminders_enabled": False}


def update_user_settings(user_id, settings):
    """
    Обновить настройки пользователя.
    :param user_id: ID пользователя.
    :param settings: Словарь с новыми настройками.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Проверяем, есть ли пользователь в таблице
    cursor.execute("SELECT 1 FROM user_settings WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        # Если пользователь есть, обновляем записи
        cursor.execute(
            "UPDATE user_settings SET reminders_enabled = ? WHERE user_id = ?",
            (settings.get("reminders_enabled", False), user_id)
        )
    else:
        # Если пользователя нет, добавляем его в таблицу
        cursor.execute(
            "INSERT INTO user_settings (user_id, reminders_enabled) VALUES (?, ?)",
            (user_id, settings.get("reminders_enabled", False))
        )

    conn.commit()
    conn.close()

def save_feedback(user_id, rating, review):
    connection = sqlite3.connect(DB_PATH)  # Замените на путь к вашей БД
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO feedback (user_id, rating, review) VALUES (?, ?, ?)",
        (user_id, rating, review),
    )
    connection.commit()
    connection.close()