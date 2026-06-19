import sqlite3

conn = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact TEXT UNIQUE
)
""")

conn.commit()


def save_message(role, message):

    cursor.execute(
        "INSERT INTO conversations(role,message) VALUES(?,?)",
        (role, message)
    )

    conn.commit()


def get_conversations():

    cursor.execute(
        "SELECT role,message FROM conversations"
    )

    return cursor.fetchall()


def clear_conversations():

    cursor.execute(
        "DELETE FROM conversations"
    )

    conn.commit()
 