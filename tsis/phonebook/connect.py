import psycopg2
import psycopg2.extras
from config import DB_CONFIG


def get_conn():
    """Return a new psycopg2 connection using DB_CONFIG."""
    return psycopg2.connect(**DB_CONFIG)


def get_cursor(conn):
    """Return a RealDictCursor for the given connection."""
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def run_sql_file(path: str):
    """Execute a .sql file against the configured database."""
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        print(f"[DB] Executed {path}")
    except Exception as e:
        conn.rollback()
        print(f"[DB] Error executing {path}: {e}")
    finally:
        conn.close()