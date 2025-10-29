from flask import Flask, render_template, request, send_file
import csv
import os

app = Flask(__name__)
DATA_FILE = "student_data.csv"

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/enroll', methods=['POST'])
def enroll():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']

    # Save to CSV
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['First Name', 'Last Name', 'Email', 'Phone'])
        writer.writerow([first_name, last_name, email, phone])

    return f"""
        <h2>Student {first_name} {last_name} enrolled successfully!</h2>
        <a href="/">Go back</a> |
        <a href="/download">📥 Download Student List</a>
    """

@app.route('/download')
def download():
    if os.path.exists(DATA_FILE):
        return send_file(DATA_FILE, as_attachment=True)
    else:
        return "<h3>No student data available yet.</h3><a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)