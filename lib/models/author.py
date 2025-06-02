import sqlite3
from .article import Article
from .magazine import Magazine

class Author:
    def __init__(self, name, id=None):
        if not isinstance(name, str) or not (0 < len(name) <= 255):
            raise ValueError("Author name must be a non-empty string up to 255 characters")
        self.name = name
        self.id = id

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"

    def save(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        if self.id is None:
            cur.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cur.lastrowid
        else:
            cur.execute("UPDATE authors SET name=? WHERE id=?", (self.name, self.id))
        conn.commit()
        conn.close()
    @classmethod
    def find_by_id(cls,id):
        conn= sqlite3.connect("project.db")
        cur= conn.cursor()
        row=cur.execute("SELECT * FROM authors WHERE id=?",(id,)).fetchone()
        conn.close()
        if row:
            return cls(name=row[1], id=row[0])
        else:
            return None
    @classmethod
    def find_by_name(cls,name):
        conn=sqlite3.connect("project.db")
        cur= conn.cursor()
        row=cur.execute("SELECT * FROM authors WHERE name = ?",(name,)).fetchone()
        conn.close()
        if row:
            return cls(name=row[1], id=row[0])
        else :
            return None


    def articles(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM articles WHERE author_id=?", (self.id,)).fetchall()
        conn.close()
        return [Article(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    def magazines(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("""
        SELECT DISTINCT m.id, m.name, m.category
        FROM articles a
        INNER JOIN magazines m ON a.magazine_id=m.id
        WHERE  a.author_id=?
        """, (self.id,)).fetchall()
        conn.close()
        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]

    def add_article(self, magazine, title):
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT DISTINCT m.category
            FROM articles a
            INNER JOIN magazines m ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,)).fetchall()
        conn.close()
        return [row[0] for row in rows]
    @classmethod
    def top_author(cls):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        row = cur.execute("""
            SELECT a.id, a.name, COUNT(ar.id) AS article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """).fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1])
        return None
    