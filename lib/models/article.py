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
    
    @classmethod
    def find_by_id(cls, article_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM articles WHERE id=?", (article_id,)).fetchone()
        conn.close()
        if row:
            return cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3])
        return None

    @classmethod
    def find_by_author(cls, author_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM articles WHERE author_id=?", (author_id,)).fetchall()
        conn.close()
        return [cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM articles WHERE magazine_id=?", (magazine_id,)).fetchall()
        conn.close()
        return [cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]
    @classmethod
    def find_by_title(cls, title):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM articles WHERE title=?", (title,)).fetchone()
        conn.close()
        if row:
            return cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3])
        return None