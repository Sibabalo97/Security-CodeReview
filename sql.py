from flask import Flask, request
import sqlite3

app = Flask(__name__)

DB_PATH = "users.db"

# Ensure table exists
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")

# Insert sample user if not exists
cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin','admin123')")

conn.commit()
conn.close()


@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #  Vulnerable SQL query 
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    if result:
        return "Logged in"
    else:
        return "Invalid login"


if __name__ == "__main__":
    app.run(debug=True)