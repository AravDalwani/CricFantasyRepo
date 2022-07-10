from flask import Flask, url_for, render_template, request, redirect
import numpy as np
import os
from flask_mail import Mail, Message
from form_contact import ContactForm, csrf, PredForm

mail = Mail()

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'newpythontestapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'yhvgoogijajxqfsi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)


def send_message(message):
    print(message.get('name'))

    msg = Message(message.get('subject'), sender = message.get('email'),
            recipients = ['newpythontestapp@gmail.com'],
            body= message.get('message')
    )
    mail.send(msg)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/success')
def success():
    return render_template('success.html')

@app.route("/contact", methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_message(request.form)
        return redirect('/')

    return render_template("contact.html", form=form)

if __name__ == "__main__":
    app.debug = True
    app.run()