from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@main.route('/success')
def success():
    return render_template('success.html')

@main.route("/contact", methods=['POST', 'GET'])
def contact():

    return render_template("contact.html")

