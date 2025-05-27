import sqlite3

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        if not isinstance(title, str) or not (0 < len(title) <= 255):
            raise ValueError("Title must be a non-empty string up to 255 characters")
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = id

    def save(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        if self.id is None:
            cur.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                        (self.title, self.author_id, self.magazine_id))
            self.id = cur.lastrowid
        else:
            cur.execute("UPDATE articles SET title=?, author_id=?, magazine_id=? WHERE id=?",
                        (self.title, self.author_id, self.magazine_id, self.id))
        conn.commit()
        conn.close()