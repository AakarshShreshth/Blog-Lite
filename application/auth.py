from flask import request, render_template, flash, url_for, redirect
from flask import current_app as app
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.database import db
from application.models import User

# Auth
# --begin
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f"Welcome! {username}", category="success")
                login_user(user)
                return redirect(url_for('.home'))
            else:
                flash('Incorrect Password.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(username=username).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("Email already in use.", category="error")
        elif username_exists:
            flash("Username already in use.", category="error")
        elif password1 != password2:
            flash("Password doesn't match!", category="error")
        elif len(username) < 3 :
            flash("Username too short.", category="error")
        elif len(password1) < 4:
            flash("Password too short.",category="error")
        elif len(email) < 11:
            flash("Invalid Email.", category="error")
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("User created!")
            return redirect(url_for(".home"))
    return render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))
# --end



# Login Manager
# --begin
login_manager = LoginManager()
login_manager.login_view = ".index"
login_manager.init_app(app)
# --end

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
