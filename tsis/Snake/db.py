import psycopg2
import psycopg2.extras
from datetime import datetime

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "snakegame",
    "user":     "postgres",
    "password": "Arkhata2007",
}


def _connect():
    """Return a new psycopg2 connection."""
    return psycopg2.connect(**DB_CONFIG)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""


def init_db():
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute(SCHEMA_SQL)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB] init_db error: {e}")
        return False


# ── Player helpers ─────────────────────────────────────────────────────────────

def get_or_create_player(username: str) -> int | None:
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        row = cur.fetchone()
        if row:
            player_id = row[0]
        else:
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id",
                (username,)
            )
            player_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return player_id
    except Exception as e:
        print(f"[DB] get_or_create_player error: {e}")
        return None


def save_session(player_id: int, score: int, level_reached: int) -> bool:
    """Insert one game-session row. Returns True on success."""
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) "
            "VALUES (%s, %s, %s)",
            (player_id, score, level_reached)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB] save_session error: {e}")
        return False


def get_personal_best(player_id: int) -> int:
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT COALESCE(MAX(score), 0) FROM game_sessions "
            "WHERE player_id = %s",
            (player_id,)
        )
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return int(result)
    except Exception as e:
        print(f"[DB] get_personal_best error: {e}")
        return 0


def get_leaderboard(limit: int = 10) -> list[dict]:
    try:
        conn = _connect()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """
            SELECT
                ROW_NUMBER() OVER (ORDER BY gs.score DESC) AS rank,
                p.username,
                gs.score,
                gs.level_reached,
                gs.played_at
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = [dict(r) for r in cur.fetchall()]
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB] get_leaderboard error: {e}")
        return []
