import sqlite3
from article import Article
from author import Author

class Magazine:
    magazine_categories = [
        "Fashion & Lifestyle", "Technology & Gadgets", "Health & Fitness",
        "News & Politics", "Business & Finance", "Entertainment & Pop Culture",
        "Travel & Adventure", "Home & Garden", "Science & Nature",
        "Food & Cooking", "Hobbies & Interests", "Literature & Culture"
    ]

    def __init__(self, name, category, id=None):
        if not isinstance(name, str) or not (0 < len(name) <= 255):
            raise ValueError("Magazine name must be a non-empty string up to 255 characters")
        if category not in Magazine.magazine_categories:
            raise ValueError("Invalid category.")
        self.name = name
        self.category = category
        self.id = id

    def save(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        if self.id is None:
            cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
            self.id = cur.lastrowid
        else:
            cur.execute("UPDATE magazines SET name=?, category=? WHERE id=?", (self.name, self.category, self.id))
        conn.commit()
        conn.close()

    def articles(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,)).fetchall()
        conn.close()
        return [Article(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    def contributors(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT DISTINCT a.id, a.name
            FROM authors a
            INNER JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,)).fetchall()
        conn.close()
        return [Author(id=row[0], name=row[1]) for row in rows]

    def article_titles(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("SELECT title FROM articles WHERE magazine_id=?", (self.id,)).fetchall()
        conn.close()
        return [row[0] for row in rows]

    def contributing_authors(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT a.id, a.name, COUNT(*) AS article_count
            FROM authors a
            INNER JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """, (self.id,)).fetchall()
        conn.close()
        return [Author(id=row[0], name=row[1]) for row in rows]
