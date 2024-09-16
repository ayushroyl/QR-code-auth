import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Path to the JSON file
VOLUNTEERS_FILE = 'volunteers.json'

# Function to load volunteer data from JSON file
def load_volunteers():
    if os.path.exists(VOLUNTEERS_FILE):
        with open(VOLUNTEERS_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

# Function to save volunteer data to JSON file
def save_volunteers(volunteers):
    with open(VOLUNTEERS_FILE, 'w') as file:
        json.dump(volunteers, file, indent=4)

# Load volunteers into memory
volunteers = load_volunteers()

@app.route('/', methods=['GET'])
def verify():
    name = request.args.get('name')
    unique_id = request.args.get('id')

    if unique_id in volunteers and volunteers[unique_id]['name'] == name:
        status_class = 'success'
        icon = 'fa-check-circle'
        message = f"Verified: {name} with ID {unique_id}"
    else:
        status_class = 'failure'
        icon = 'fa-times-circle'
        message = "Verification failed: Invalid name or ID"

    return render_template('index.html', status_class=status_class, icon=icon, message=message)

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Hardcoded admin credentials (replace with a secure authentication system in production)
    if username == "admin" and password == "password123":
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/admin-dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        name = request.form.get('name')
        unique_id = request.form.get('unique_id')

        if name and unique_id:
            # Add the new volunteer to the dictionary
            volunteers[unique_id] = {"name": name, "id_no": unique_id}
            # Save the updated data to the JSON file
            save_volunteers(volunteers)
            return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html', volunteers=volunteers)

if __name__ == "__main__":
    app.run(debug=True)
