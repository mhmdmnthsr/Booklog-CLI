import click
import json
import os
from datetime import date , datetime 
from tabulate import tabulate
import csv

DATA_FILE = "books.json"

def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_books(books):
    with open(DATA_FILE, "w") as f:
        json.dump(books, f, indent=2)

@click.group()
def main():
    pass

@main.command()
@click.argument("title")
@click.option("--author", required=True, help="Author of the book")
@click.option("--pages", type=int, required=True, help="Total number of pages")
@click.option("--status", default="Not Started", help="Status of the book")
def add(title, author, pages, status):
    books = load_books()


    next_id = books[-1]["id"] + 1 if books else 1

    book = {
        "id": next_id,
        "title": title,
        "author": author,
        "pages": pages,
        "status": status,
        "progress": 0  
    }

    books.append(book)
    save_books(books)

    print(f"✅ Book added: {title} by {author} (ID: {next_id})")


@main.command()
@click.argument("book_id" ,type=int)
def start(book_id):
    books = load_books()
    
    for book in books:
        if book["id"] == book_id:
            book["status"] = "reading"
            book["started"] = date.today().strftime("%d-%m-%Y")
            save_books(books)
            print(f'📖 Started reading "{book["title"]}" on {book["started"]}')
            return


    print(f"❌ Book with ID {book_id} not found.")

@main.command()
@click.argument("book_id" , type=int)
@click.option("--pages" ,type=int ,required=True ,help="give the progress done in pages")
def update(book_id ,pages):
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            if book["status"] == "Not Started":
                print(f"⚠️ You need to start the book before updating progress.")
                return
            if pages > book["pages"]:
                print(f"❌ Page {pages} is more than total pages of the book ({book['pages']})")
                return
            if "progress_log" not in book:
                book["progress_log"] = []

            today = date.today().strftime("%d-%m-%Y")
            book["progress_log"].append({"date": today, "page": pages})

            book["progress"] = pages

            percent = (pages / book["pages"]) * 100
            save_books(books)

            if pages == book["pages"]:
                book["status"] = "finished"
                book["finished"] = date.today().strftime("%d-%m-%Y")
                print(f'📈 Updated: Now at page {pages} of {book["pages"]} ({percent:.1f}% complete)')
                print(f'🎉 You’ve finished reading "{book["title"]}" on {book["finished"]}!')
            else:
                print(f'📈 Updated: Now at page {pages} of {book["pages"]} ({percent:.1f}% complete)')
            return

    print(f"❌ Book with ID {book_id} not found.")


@main.command()
@click.argument("book_id", type=int)
def finish(book_id):
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            if book.get("status") =="Not Started":
                print(f"⚠️ You haven't started this book yet.")
                return

            if "started" not in book:
                print("❌ No start date found. Cannot finish.")
                return

            if book["progress"] < book["pages"]:
                print(f"⚠️ You are only on page {book['progress']} of {book['pages']}. Finish reading first")
                return

            start_date = datetime.strptime(book["started"], "%d-%m-%Y").date()
            finish_date = date.today()
            duration = (finish_date - start_date).days

            book["status"] = "finished"
            book["finished"] = finish_date.strftime("%d-%m-%Y")
            save_books(books)

            print(f'✅ Finished "{book["title"]}" on {book["finished"]}')
            print(f'📊 Total time taken: {duration} days')
            return

    print(f"❌ Book with ID {book_id} not found.")


@main.command()
@click.argument("book_id", type=int)
def remove(book_id):
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            confirm = input(f"❗ Are you sure you want to remove '{book['title']}'? (y/N): ")
            if confirm() == "y" or "Y":
                books.remove(book)
                save_books(books)
                print(f"🗑️ Removed book: {book['title']} (ID: {book_id})")
            else:
                print("❎ Cancelled.")
            return

    print(f"❌ Book with ID {book_id} not found.")


@main.command()
def list():
    books = load_books()

    if not books:
        print("📭 No books found. Add one using `booklog add`.")
        return

    table = []
    for book in books:
        progress = f"{book.get('progress', 0)}/{book['pages']}"
        percent = (book.get("progress", 0) / book["pages"]) * 100
        row = [
            book["id"],
            book["title"],
            book["author"],
            progress,
            book["status"],
            f"{percent:.1f}%"
        ]
        table.append(row)

    headers = ["ID", "Title", "Author", "Progress", "Status", "% Read"]
    print("📚 Your Books:")
    print(tabulate(table, headers=headers, tablefmt="grid"))

@main.command()
def stats():
    books = load_books()

    if not books:
        print("📭 No books in the system.")
        return

    total = len(books)
    reading = sum(1 for b in books if b["status"] == "reading")
    finished = sum(1 for b in books if b["status"] == "finished")
    not_started = sum(1 for b in books if b["status"] == "Not Started")

    print("📈 Reading Stats:")
    print(f"• Total books: {total}")
    print(f"• Not Started: {not_started} | Reading: {reading} | Finished: {finished}")
    fastest = None
    fastest_days = float('inf')
    total_pages = 0
    total_days = 0

    for book in books:
        if book["status"] == "finished" and "started" in book and "finished" in book:
            start = datetime.strptime(book["started"], "%d-%m-%Y").date()
            end = datetime.strptime(book["finished"], "%d-%m-%Y").date()
            days = (end - start).days or 1  # prevent division by 0

            # Track fastest
            if days < fastest_days:
                fastest_days = days
                fastest = book["title"]

            # For average calculation
            total_pages += book["pages"]
            total_days += days

    if fastest:
        print(f"• Fastest finish: {fastest} ({fastest_days} days)")

    if total_days > 0:
        avg_pages = total_pages / total_days
        print(f"• Average pages/day: {avg_pages:.1f}")

@main.command()
@click.option("--format", type=click.Choice(["json", "csv"]), required=True, help="Export format")
@click.option("--out", required=True, help="Output filename")
def export(format, out):
    books = load_books()

    if not books:
        print("📭 No books to export.")
        return

    if format == "json":
        with open(out, "w") as f:
            json.dump(books, f, indent=2)
        print(f"✅ Exported books to {out}")

    elif format == "csv":
        with open(out, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "title", "author", "pages", "progress", "status", "started", "finished"]
            )
            writer.writeheader()
            for book in books:
                writer.writerow({
                    "id": book.get("id"),
                    "title": book.get("title"),
                    "author": book.get("author"),
                    "pages": book.get("pages"),
                    "progress": book.get("progress", 0),
                    "status": book.get("status"),
                    "started": book.get("started", ""),
                    "finished": book.get("finished", "")
                })
        print(f"✅ Exported books to {out}")

                

if __name__ == "__main__":
    main()
