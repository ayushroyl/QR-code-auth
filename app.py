from flask import Flask, render_template, request, redirect, url_for, flash
import json, os

app = Flask(__name__)
volunteers = {
    "vol1": {"name": "Ayush Roy", "id_no": "vol1"},
    "vol2": {"name": "John Doe", "id_no": "vol2"},
    # Add more volunteers here
}
@app.route('/', methods=['GET'])
def verify():
    # Get the name and id from the query parameters (scanned QR code URL)
    name = request.args.get('name')
    unique_id = request.args.get('id')

    # Check if the unique_id exists in the database and matches with the name
    if unique_id in volunteers and volunteers[unique_id]['name'] == name and volunteers[unique_id]['id_no'] == unique_id:
        status_class = 'success'
        icon = 'fa-check-circle'
        message = f"Verified: {name} with ID {unique_id}"
    else:
        status_class = 'failure'
        icon = 'fa-times-circle'
        message = "Verification failed: Invalid name or ID"

    # Render the verify.html page with the result
    return render_template('index.html', status_class=status_class, icon=icon, message=message)


if __name__ == "__main__":
    app.run()
