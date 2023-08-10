from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .util import validate_email, validate_password

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user_name = request.form.get('userName')
        password = request.form.get('password')
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password.", category="error")
        else:
            flash("User not found!", category= "error")

    return render_template("login.html", user= current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_name = request.form.get("userName")
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        pwd1 = request.form.get("password1")
        pwd2 = request.form.get("password2")
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            flash("User already exists!", category="error")
        elif len(user_name) < 3:
            flash("User name should be greater than 3 characters.", category="error")
        
        elif validate_email(email):
            flash("Inavlid email.", category="error")
        elif len(first_name) < 3:
            flash("First name should be greater than 3 characters.", category="error")
        elif validate_password(pwd1):
            flash("Password doesn't meet the criteria.", category="error")
        elif validate_password(pwd2):
            flash("Confirm password doesn't meet the criteria.", category="error")
        elif pwd1 != pwd2:
            flash("Password doesn't match.", category="error")
        else:
            new_user = User(
                user_name = user_name,
                email = email,
                first_name = first_name,
                password = generate_password_hash(pwd1, method="sha256")
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created.", category="success")
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("signup.html", user= current_user)