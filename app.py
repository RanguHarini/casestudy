from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "notes.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    folder = os.path.dirname(DB_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, subject TEXT NOT NULL, content TEXT NOT NULL
        )''')

@app.route("/")
def home():
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        subjects = conn.execute("SELECT COUNT(DISTINCT subject) FROM notes").fetchone()[0]
    return render_template("index.html", count=count, subjects=subjects)

@app.route("/add", methods=["GET", "POST"])
def add_note():
    error = None
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "").strip()
        content = request.form.get("content", "").strip()
        if title and subject and content:
            with get_db() as conn:
                conn.execute("INSERT INTO notes (title, subject, content) VALUES (?, ?, ?)",
                             (title, subject, content))
            return redirect(url_for("view_notes"))
        error = "Please complete all fields."
    return render_template("add_note.html", error=error)

@app.route("/notes")
def view_notes():
    with get_db() as conn:
        notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return render_template("notes.html", notes=notes)

@app.route("/search")
def search_notes():
    query = request.args.get("q", "").strip()
    pattern = f"%{query}%"
    with get_db() as conn:
        notes = conn.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR subject LIKE ? OR content LIKE ? ORDER BY id DESC",
            (pattern, pattern, pattern)).fetchall()
    return render_template("search.html", notes=notes, query=query)

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    with get_db() as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    return redirect(url_for("view_notes"))

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

initialize_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
