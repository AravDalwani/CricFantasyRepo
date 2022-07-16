from website import create_app
from flask_mail import Mail, Message
from website import form_contact
import numpy as np
import os

app = create_app()

mail = Mail()

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
form_contact.csrf.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'newpythontestapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'yhvgoogijajxqfsi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)


if __name__ == "__main__":
    app.debug = True
    app.run()
