# ============================================================
#   GINGERY — database.py
#   MySQL connection pool, table definitions, and all helpers
# ============================================================

import os
import logging
import mysql.connector
from mysql.connector import pooling, Error

log = logging.getLogger("Gingery.DB")

# ── Pool ──────────────────────────────────────────────────────
_pool: pooling.MySQLConnectionPool | None = None


def init_pool() -> None:
    global _pool
    config = {
        "pool_name":       "gingery_pool",
        "pool_size":       5,
        "host":            os.environ["DB_HOST"],
        "port":            int(os.environ.get("DB_PORT", 3306)),
        "user":            os.environ["DB_USER"],
        "password":        os.environ["DB_PASSWORD"],
        "database":        os.environ["DB_NAME"],
        "connect_timeout": 10,
        "autocommit":      True,
    }
    try:
        _pool = pooling.MySQLConnectionPool(**config)
        log.info("MySQL connection pool created.")
    except Error as e:
        log.critical(f"Failed to create MySQL pool: {e}")
        raise


def get_connection():
    if _pool is None:
        raise RuntimeError("DB pool not initialised — call init_pool() first.")
    return _pool.get_connection()


# ── DDL ───────────────────────────────────────────────────────

_TABLES = [
    # Users registry
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id    BIGINT       NOT NULL,
        guild_id   BIGINT       NOT NULL,
        username   VARCHAR(64)  NOT NULL,
        joined_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, guild_id)
    )
    """,
    # Game stats + economy
    """
    CREATE TABLE IF NOT EXISTS stats (
        user_id          BIGINT  NOT NULL,
        guild_id         BIGINT  NOT NULL,
        trivia_wins      INT     DEFAULT 0,
        trivia_played    INT     DEFAULT 0,
        highlow_wins     INT     DEFAULT 0,
        highlow_played   INT     DEFAULT 0,
        scramble_wins    INT     DEFAULT 0,
        scramble_played  INT     DEFAULT 0,
        rps_wins         INT     DEFAULT 0,
        rps_played       INT     DEFAULT 0,
        riddle_wins      INT     DEFAULT 0,
        riddle_played    INT     DEFAULT 0,
        copypaste_played INT     DEFAULT 0,
        best_copypaste   FLOAT   DEFAULT 0.0,
        coins            INT     DEFAULT 0,
        total_xp         INT     DEFAULT 0,
        PRIMARY KEY (user_id, guild_id),
        FOREIGN KEY (user_id, guild_id)
            REFERENCES users (user_id, guild_id) ON DELETE CASCADE
    )
    """,
    # Daily reward tracking
    """
    CREATE TABLE IF NOT EXISTS daily_claims (
        user_id     BIGINT  NOT NULL,
        guild_id    BIGINT  NOT NULL,
        last_claim  DATE    NOT NULL,
        streak      INT     DEFAULT 1,
        PRIMARY KEY (user_id, guild_id),
        FOREIGN KEY (user_id, guild_id)
            REFERENCES users (user_id, guild_id) ON DELETE CASCADE
    )
    """,
]

_ALLOWED_COLS = {
    "trivia_wins", "trivia_played",
    "highlow_wins", "highlow_played",
    "scramble_wins", "scramble_played",
    "rps_wins", "rps_played",
    "riddle_wins", "riddle_played",
    "copypaste_played",
    "coins", "total_xp",
}


def create_tables() -> None:
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        for ddl in _TABLES:
            cur.execute(ddl)
        cur.close()
        log.info("Tables verified / created.")
        _migrate(conn)
    except Error as e:
        log.error(f"create_tables: {e}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()


# Columns that may be missing on existing installs: (sql_type, default_clause)
_MIGRATIONS = {
    "riddle_wins":      ("INT",   "DEFAULT 0"),
    "riddle_played":    ("INT",   "DEFAULT 0"),
    "copypaste_played": ("INT",   "DEFAULT 0"),
    "best_copypaste":   ("FLOAT", "DEFAULT 0.0"),
    "total_xp":         ("INT",   "DEFAULT 0"),
}


def _migrate(conn) -> None:
    """Safely add any columns missing from the live stats table."""
    try:
        cur = conn.cursor()
        cur.execute("SHOW COLUMNS FROM stats")
        existing = {row[0] for row in cur.fetchall()}
        for col, (col_type, default) in _MIGRATIONS.items():
            if col not in existing:
                cur.execute(
                    f"ALTER TABLE stats ADD COLUMN {col} {col_type} {default}"
                )
                log.info(f"Migration: added column stats.{col}")
        cur.close()
    except Error as e:
        log.error(f"_migrate: {e}")


# ── User bootstrap ────────────────────────────────────────────

def ensure_user(user_id: int, guild_id: int, username: str) -> None:
    """Upsert user + stats rows. Safe to call before every command."""
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "INSERT IGNORE INTO users (user_id, guild_id, username) VALUES (%s, %s, %s)",
            (user_id, guild_id, username),
        )
        cur.execute(
            "INSERT IGNORE INTO stats (user_id, guild_id) VALUES (%s, %s)",
            (user_id, guild_id),
        )
        # Keep username fresh
        cur.execute(
            "UPDATE users SET username = %s WHERE user_id = %s AND guild_id = %s",
            (username, user_id, guild_id),
        )
        cur.close()
    except Error as e:
        log.error(f"ensure_user {user_id}: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()


# ── Stat helpers ──────────────────────────────────────────────

def increment_stat(user_id: int, guild_id: int, column: str, amount: int = 1) -> None:
    """Increment an integer stats column by `amount`."""
    if column not in _ALLOWED_COLS:
        raise ValueError(f"'{column}' is not a whitelisted stats column.")
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            f"UPDATE stats SET {column} = {column} + %s "
            f"WHERE user_id = %s AND guild_id = %s",
            (amount, user_id, guild_id),
        )
        cur.close()
    except Error as e:
        log.error(f"increment_stat {column}/{user_id}: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()


def update_best_copypaste(user_id: int, guild_id: int, elapsed: float) -> bool:
    """
    Update best_copypaste if `elapsed` is a new personal best.
    Returns True if it was a new record.
    """
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            "SELECT best_copypaste FROM stats WHERE user_id = %s AND guild_id = %s",
            (user_id, guild_id),
        )
        row = cur.fetchone()
        current_best = row[0] if row else 0.0
        is_new_record = (current_best == 0.0) or (elapsed < current_best)
        if is_new_record:
            cur.execute(
                "UPDATE stats SET best_copypaste = %s "
                "WHERE user_id = %s AND guild_id = %s",
                (elapsed, user_id, guild_id),
            )
        cur.close()
        return is_new_record
    except Error as e:
        log.error(f"update_best_copypaste {user_id}: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_stats(user_id: int, guild_id: int) -> dict | None:
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT s.*, u.username, u.joined_at "
            "FROM stats s JOIN users u USING (user_id, guild_id) "
            "WHERE s.user_id = %s AND s.guild_id = %s",
            (user_id, guild_id),
        )
        row = cur.fetchone()
        cur.close()
        return row
    except Error as e:
        log.error(f"get_stats {user_id}: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()


# ── Leaderboard ───────────────────────────────────────────────

_LB_COLS = {
    "coins":       ("🪙 Coins",        "coins"),
    "total_xp":    ("⭐ Total XP",      "total_xp"),
    "trivia":      ("🧠 Trivia Wins",   "trivia_wins"),
    "highlow":     ("🔢 High-Low Wins", "highlow_wins"),
    "scramble":    ("🔀 Scramble Wins", "scramble_wins"),
    "rps":         ("✂️ RPS Wins",      "rps_wins"),
    "riddle":      ("🔍 Riddle Wins",   "riddle_wins"),
    "copypaste":   ("⌨️ Best Typing",   "best_copypaste"),
}

LB_CHOICES = list(_LB_COLS.keys())   # exposed to gingery.py for app_commands.choices


def get_leaderboard(guild_id: int, category: str, limit: int = 10) -> list[dict]:
    """
    Returns up to `limit` rows ordered by the chosen stat column.
    Each row has: rank, username, value.
    """
    if category not in _LB_COLS:
        raise ValueError(f"Unknown leaderboard category: {category}")

    label, col = _LB_COLS[category]
    # copypaste is ASC (lower = better); everything else DESC
    order = "ASC" if category == "copypaste" else "DESC"
    # exclude rows where the stat is still 0 / 0.0
    nonzero = f"AND s.{col} > 0"

    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)
        cur.execute(
            f"""
            SELECT u.username, s.{col} AS value,
                   RANK() OVER (ORDER BY s.{col} {order}) AS rank
            FROM stats s
            JOIN users u USING (user_id, guild_id)
            WHERE s.guild_id = %s {nonzero}
            ORDER BY s.{col} {order}
            LIMIT %s
            """,
            (guild_id, limit),
        )
        rows = cur.fetchall()
        cur.close()
        return rows, label
    except Error as e:
        log.error(f"get_leaderboard {category}: {e}")
        return [], label
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_rank(user_id: int, guild_id: int, category: str) -> int | None:
    """Returns the calling user's rank for a given category, or None."""
    if category not in _LB_COLS:
        return None
    label, col = _LB_COLS[category]
    order = "ASC" if category == "copypaste" else "DESC"
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            f"""
            SELECT user_rank FROM (
                SELECT user_id,
                       RANK() OVER (ORDER BY {col} {order}) AS user_rank
                FROM stats
                WHERE guild_id = %s AND {col} > 0
            ) ranked
            WHERE user_id = %s
            """,
            (guild_id, user_id),
        )
        row = cur.fetchone()
        cur.close()
        return row[0] if row else None
    except Error as e:
        log.error(f"get_rank {category}/{user_id}: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()


# ── Daily reward ──────────────────────────────────────────────

def claim_daily(user_id: int, guild_id: int) -> dict:
    """
    Attempt a daily coins claim.
    Returns:
        {
            "claimed": bool,
            "coins":   int,        # coins awarded this claim
            "streak":  int,        # current streak
            "next_in": str | None, # "HH:MM:SS" until next claim, or None
        }
    """
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor(dictionary=True)

        # Check existing claim
        cur.execute(
            "SELECT last_claim, streak FROM daily_claims "
            "WHERE user_id = %s AND guild_id = %s",
            (user_id, guild_id),
        )
        row = cur.fetchone()

        from datetime import date, timedelta
        today = date.today()

        if row:
            last = row["last_claim"]  # already a date object from MySQL
            if last == today:
                # Already claimed today
                cur.close()
                return {"claimed": False, "coins": 0, "streak": row["streak"], "next_in": "tomorrow"}

            streak = row["streak"] + 1 if last == today - timedelta(days=1) else 1
            cur.execute(
                "UPDATE daily_claims SET last_claim = %s, streak = %s "
                "WHERE user_id = %s AND guild_id = %s",
                (today, streak, user_id, guild_id),
            )
        else:
            streak = 1
            cur.execute(
                "INSERT INTO daily_claims (user_id, guild_id, last_claim, streak) "
                "VALUES (%s, %s, %s, 1)",
                (user_id, guild_id, today),
            )

        # Coins formula: base 100 + 20 per streak day, capped at 500
        coins = min(100 + (streak - 1) * 20, 500)
        xp    = coins // 5

        cur.execute(
            "UPDATE stats SET coins = coins + %s, total_xp = total_xp + %s "
            "WHERE user_id = %s AND guild_id = %s",
            (coins, xp, user_id, guild_id),
        )
        cur.close()
        return {"claimed": True, "coins": coins, "streak": streak, "next_in": None}

    except Error as e:
        log.error(f"claim_daily {user_id}: {e}")
        return {"claimed": False, "coins": 0, "streak": 0, "next_in": None}
    finally:
        if conn and conn.is_connected():
            conn.close()


# ── Ping ──────────────────────────────────────────────────────

def ping() -> tuple[bool, str]:
    conn = None
    try:
        conn = get_connection()
        info = conn.get_server_info()
        cur  = conn.cursor()
        cur.execute("SELECT DATABASE();")
        db_name = cur.fetchone()[0]
        cur.close()
        return True, f"MySQL {info} — database: `{db_name}`"
    except Error as e:
        return False, str(e)
    finally:
        if conn and conn.is_connected():
            conn.close()