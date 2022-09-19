from flask import Blueprint, render_template
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Match, User
from app import db

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

@main.route("/betting", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        #match = Post(input=text, player_id=current_user.id)
        db.session.add()
        db.session.commit()
        
        #flash('Post created!', category='success')

        return redirect(url_for('auth.success'))

    return render_template('betting.html', user=current_user)
