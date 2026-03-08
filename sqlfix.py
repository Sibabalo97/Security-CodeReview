from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# Ensure database exists with a sample user
DB_PATH = "users.db"
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
    conn.commit()
    conn.close()

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    if not username or not password:
        return "Username and password required", 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #  Use parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    conn.close()

    if result:
        return "Logged in"
    else:
        return "Invalid login"

# Start the Flask server outside route
if __name__ == "__main__":
    app.run(debug=True)