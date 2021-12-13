import sqlite3


def displaydata():
    conn = sqlite3.connect('DV')

    cur = conn.cursor()
    cur.execute("SELECT * FROM Driver")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.execute("SELECT * FROM Vehicle")

    rows = cur.fetchall()

    for row in rows:
        print(row)
