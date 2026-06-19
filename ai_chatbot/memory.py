from database import cursor, conn


def save_memory(text):

    cursor.execute(
        "SELECT fact FROM memory WHERE fact=?",
        (text,)
    )

    if cursor.fetchone() is None:

        cursor.execute(
            "INSERT INTO memory(fact) VALUES(?)",
            (text,)
        )

        conn.commit()


def get_memories():

    cursor.execute(
        "SELECT fact FROM memory ORDER BY id DESC LIMIT 10"
    )

    return [
        row[0]
        for row in cursor.fetchall()
    ]


def clear_memory():

    cursor.execute(
        "DELETE FROM memory"
    )

    conn.commit()