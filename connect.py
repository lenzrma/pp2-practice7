import psycopg2
from config import db_config

def get_connection():
    """Установка соединения с базой данных PostgreSQL."""
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as error:
        print(f"Ошибка подключения к базе данных: {error}")
        return None

def create_tables():
    """Создание таблицы contacts, если она отсутствует."""
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL
                );
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("Таблица 'contacts' успешно создана (или уже существует).")
        except Exception as error:
            print(f"Ошибка при создании таблицы: {error}")

if __name__ == "__main__":
    create_tables()