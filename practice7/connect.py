import psycopg2
from config import db_config

def get_db_connection():
    """Устанавливает соединение с БД."""
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def create_tables():
    """Создает таблицу contacts, если её нет (Design table)."""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    user_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL
                )
            """)
        conn.commit()
        print("Таблица 'contacts' готова.")
    except Exception as e:
        print(f"Ошибка создания таблицы: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    create_tables()