import sqlite3
import csv
from io import StringIO
from flask import Flask, render_template, request, redirect, url_for, make_response

# Application Initialize
app = Flask(__name__)

# --- Database Utility Function ---
def get_db_connection():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row  
    return conn

# --- Database Setup Logic ---
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')
    
    # 2. Transactions Table
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
    
    # 3. Sample User and Data Create karo
    cursor.execute("SELECT * FROM users WHERE username = 'Shubham Yadav'")
    user = cursor.fetchone()
    if not user:
        # User banao
        cursor.execute("INSERT INTO users (username, password, balance) VALUES ('Shubham Yadav', '1234', 50450.00)")
        user_id = cursor.lastrowid
        
        # Transactions daalo
        cursor.execute("INSERT INTO transactions (user_id, date, description, amount, status) VALUES (?, ?, ?, ?, ?)", (user_id, '01 Dec 2025', 'Salary Credit', 45000.00, 'Completed'))
        cursor.execute("INSERT INTO transactions (user_id, date, description, amount, status) VALUES (?, ?, ?, ?, ?)", (user_id, '28 Nov 2025', 'Grocery Store', -2300.00, 'Completed'))
        cursor.execute("INSERT INTO transactions (user_id, date, description, amount, status) VALUES (?, ?, ?, ?, ?)", (user_id, '25 Nov 2025', 'Electric Bill', -850.00, 'Pending'))
        print("Sample Data Created Successfully!")

    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        username_input = request.form.get('username')
        password_input = request.form.get('password')
    else:
        # Logout se redirect hone par login page par bhej denge
        return redirect(url_for('login')) 

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # User check karo
    cursor.execute("SELECT * FROM users WHERE username = ?", (username_input,))
    user = cursor.fetchone()

    # Authentication
    if user and user['password'] == password_input:
        user_id = user['id']
        current_balance = user['balance']
        
        # Transactions fetch karo
        cursor.execute("SELECT date, description, amount, status FROM transactions WHERE user_id = ?", (user_id,))
        user_transactions = cursor.fetchall()
        conn.close()

        return render_template('dashboard.html', 
                               user=username_input, 
                               balance=current_balance, 
                               transactions=user_transactions)
    else:
        conn.close()
        return "<h1>Login Failed!</h1><a href='/'>Try Again</a>"


@app.route('/download')
def download_statement():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Shubham Yadav ka data nikalo
    cursor.execute("SELECT id FROM users WHERE username = 'Shubham Yadav'")
    user_id = cursor.fetchone()['id']
    
    cursor.execute("SELECT date, description, amount, status FROM transactions WHERE user_id = ?", (user_id,))
    transactions = cursor.fetchall()
    conn.close()

    # CSV File banana
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Description', 'Amount', 'Status'])
    
    for row in transactions:
        cw.writerow([row['date'], row['description'], row['amount'], row['status']])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=financial_statement.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output


@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)