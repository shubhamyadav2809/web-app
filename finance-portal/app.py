from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)

# --- ROUTE 1: Login Page (Home) ---
# This route handles the initial landing page request.
# When the user visits the root URL ('/'), the login page is displayed.
@app.route('/')
def login():
    # Render the login.html template located in the templates folder.
    return render_template('login.html')

# --- ROUTE 2: Dashboard (Post-Login) ---
# This route handles the form submission from the login page.
# It listens for POST requests sent to '/dashboard'.
@app.route('/dashboard', methods=['POST'])
def dashboard():
    # Retrieve the username and password entered by the user in the form.
    username = request.form.get('username')
    password = request.form.get('password')

    # In a real-world production scenario, we would verify these credentials 
    # against a secure database using hashing algorithms.
    # For this prototype, we are simulating a successful login to demonstrate the flow.
    
    # Return a welcome message with the username to confirm successful access.
    return f"<h1>Welcome to Client Dashboard, {username}!</h1><p>Login Successful.</p>"

# --- Main Execution ---
# Check if this script is executed directly (not imported).
if __name__ == '__main__':
    # Start the Flask development server.
    # debug=True allows the server to auto-reload on code changes and show errors.
    print("🚀 Project Started! Access at: [http://127.0.0.1:5000](http://127.0.0.1:5000)")
    app.run(debug=True)