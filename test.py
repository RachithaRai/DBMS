import sqlite3
def test():
    with sqlite3.connect("file.db") as conn:
        c = conn.cursor()

        c.execute("ALTER TABLE client DROP clientusername ")

test()