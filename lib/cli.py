import sqlite3
from models.author import Author
from models.magazine import Magazine
from models.article import Article

def main():
    while True:
        print("\n📰 Magazine CLI")
        print("1. List Authors")
        print("2. List Magazines")
        print("3. List Articles")
        print("4. Add Author")
        print("5. Add Magazine")
        print("6. Add Article")
        print("7. Find Top Publisher")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            list_authors()
        elif choice == "2":
            list_magazines()
        elif choice == "3":
            list_articles()
        elif choice == "4":
            add_author()
        elif choice == "5":
            add_magazine()
        elif choice == "6":
            add_article()
        elif choice == "7":
            top_publisher()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

def list_authors():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    for row in cur.execute("SELECT * FROM authors"):
        print(row)
    conn.close()

def list_magazines():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    for row in cur.execute("SELECT * FROM magazines"):
        print(row)
    conn.close()

def list_articles():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    for row in cur.execute("SELECT * FROM articles"):
        print(row)
    conn.close()

def add_author():
    name = input("Author name: ")
    author = Author(name=name)
    author.save()
    print("Author added:", author)

def add_magazine():
    name = input("Magazine name: ")
    category = input("Category: ")
    magazine = Magazine(name=name, category=category)
    magazine.save()
    print("Magazine added:", magazine)

def add_article():
    title = input("Article title: ")
    author_id = int(input("Author ID: "))
    magazine_id = int(input("Magazine ID: "))
    article = Article(title=title, author_id=author_id, magazine_id=magazine_id)
    article.save()
    print("Article added:", article)

def top_publisher():
    top = Magazine.top_publisher()
    print("Top Publisher:", top)

if __name__ == "__main__":
    main()