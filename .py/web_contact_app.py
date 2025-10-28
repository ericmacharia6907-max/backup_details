from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        # Collect form data
        name = request.form['name']
        email = request.form['email']
        message_text = request.form['message']
        phone = request.form['phone']
        # Save data to file
        with open('contacts.txt', 'a') as f:
            f.write(f"{name},{email},{message_text},{phone}\n")
        # Set success message
        message = "Thank You! Your details have been saved."
    # Render template and pass message
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
