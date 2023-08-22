create_user_table_query = """
        CREATE TABLE IF NOT EXISTS telegram_users
        (ID INTEGER PRIMARY KEY,
        TELEGRAM_ID INTEGER,
        USERNAME CHAR(50),
        FIRST_NAME CHAR (50),
        LAST_NAME CHAR(50)
        )
"""

start_insert_user_query = """INSERT OR IGNORE INTO telegram_users VALUES (?,?,?,?,?)"""


