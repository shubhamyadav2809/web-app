import sqlite3
from flask import Flask, render_template, request, redirect, url_for

# Application Initialize (Dhyan dein: __name__ mein DO underscores hain)
app = Flask(__name__)

# --- Database Setup Logic ---
def init_db():
    # Database connection banayenge (finance.db file ban jayegi)
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Users table banayenge agar nahi hai
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')
    
    # Transactions table banayenge
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            description TEXT,
            amount REAL,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Sample User Create karenge (Agar pehle se nahi hai)
    cursor.execute("SELECT * FROM users WHERE username = 'Shubham Yadav'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, balance) VALUES ('Shubham Yadav', '1234', 50450.00)")
        print("Sample User Created: Shubham Yadav / 1234")

    conn.commit()
    conn.close()

# App start hone par database initialize karo
init_db()

# --- ROUTE 1: Login Page ---
@app.route('/')
def login():
    return render_template('login.html')

# --- ROUTE 2: Dashboard Logic (Database Connected) ---
@app.route('/dashboard', methods=['POST'])
def dashboard():
    username_input = request.form.get('username')
    password_input = request.form.get('password')

    # Database se check karenge
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # User dhoondenge
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username_input, password_input))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Login Successful - Pass username to dashboard
        return render_template('dashboard.html', user=username_input)
    else:
        # Login Failed
        return "<h1>Login Failed! Incorrect Username or Password.</h1><a href='/'>Try Again</a>"

# --- Main Execution ---
# (Yahan bhi __name__ aur __main__ mein DO underscores hone chahiye)
if __name__ == '__main__':
    print("🚀 Project Started with Database! Access at: http://127.0.0.1:5000")
    app.run(debug=True)