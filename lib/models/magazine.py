import sqlite3


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
    def __repr__(self):
        return f"<Magazine id={self.id} name='{self.name}' category='{self.category}'>"
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
        from .article import Article
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,)).fetchall()
        conn.close()
        return [Article(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    def contributors(self):
        from .author import Author
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
        from .author import Author
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
    @classmethod
    def find_by_id(cls, mag_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM magazines WHERE id=?", (mag_id,)).fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM magazines WHERE name=?", (name,)).fetchone()
        conn.close()
        if row:
            return cls(id=row[0], name=row[1], category=row[2])
        return None
    
    @classmethod
    def find_by_category(cls, category):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM magazines WHERE category=?", (category,)).fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], category=row[2]) for row in rows]
    
    def  top_publisher(cls):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        row= cur.execute(
            """
            SELECT m.id,m.name, m.category, COUNT(*) AS count
            FROM articles a 
            INNER JOIN magazines m ON m.id= a.magazine_id
            GROUP BY m.id
            ORDER BY count DESC
            LIMIT 1
        """
        ).fetchone()
        conn.close()
        if row:
            return cls(name=row[1],category=row[2],id=row[0])
        else :
            return None