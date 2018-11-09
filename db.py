import sqlite3


class SQLite():
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row

        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


class DBRequest():
    def __init__(self, sqlite):
        self.sqlite = sqlite

    def create(self):
        with self.sqlite as db:
            db.execute("""
        CREATE TABLE IF NOT EXISTS post (
          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          channel_id INTEGER NOT NULL,
          post_id INTEGER NOT NULL,
          like_yes INTEGER NOT NULL,
          like_not INTEGER NOT NULL
        )
      """)

    def new_post(self, data):
        with self.sqlite as db:
            db.execute("INSERT INTO post VALUES (?, ?, ?, ?, ?)", data)

    def select_post(self, data):
        with self.sqlite as db:
            db.execute("SELECT * FROM post WHERE channel_id = ? AND post_id = ? LIMIT 1", data)

            return db.fetchall()

    def new_like_yes(self, data):
        with self.sqlite as db:
            db.execute("UPDATE post SET like_yes = ? WHERE channel_id = ? AND post_id = ?", data)

    def new_like_not(self, data):
        with self.sqlite as db:
            db.execute("UPDATE post SET like_not = ? WHERE channel_id = ? AND post_id = ?", data)
