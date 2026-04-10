import psycopg2
from config import db_config
import os

def get_db_connection():
    try:
        return psycopg2.connect(**db_config)
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def setup_database():
    conn = get_db_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    user_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL
                )
            """)
            
            if os.path.exists('functions.sql'):
                with open('functions.sql', 'r', encoding='utf-8') as f:
                    cur.execute(f.read())
                    
            if os.path.exists('procedures.sql'):
                with open('procedures.sql', 'r', encoding='utf-8') as f:
                    cur.execute(f.read())
                    
        conn.commit()
        print("База данных, функции и процедуры успешно инициализированы!")
    except Exception as e:
        print(f"Ошибка настройки БД: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    setup_database()