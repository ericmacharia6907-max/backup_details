from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def backup_details():
    message = ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        phone = request.form['phone']
        email = request.form['email']

        # Save details in a file (append mode)
        with open('backup_contacts.txt', 'a') as f:
            f.write(f"{first_name},{second_name},{phone},{email}\n")

        message = "Thank You! Your backup details have been saved."

    return render_template('backup.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
