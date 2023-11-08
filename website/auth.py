from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Record, UserType
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import sqlalchemy as sa
from flask_login import login_user, logout_user, login_required, current_user

authBP = Blueprint('authBP', __name__, static_folder='./static/', template_folder='./templates/')

@authBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = db.session.execute(sa.select(User).filter_by(email=email)).first()
        if result:
            user: User = result.User
            if check_password_hash(user.pwhash, password):
                # log in successfully
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('viewsBP.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template('login.html', user=current_user)

@authBP.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authBP.login'))

@authBP.route('/')
def index():
    return redirect(url_for('authBP.login'))

@authBP.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = request.form
        email = form['email']
        name = form['name']
        password1 = form['password1']
        password2 = form['password2']

        if password1 != password2:
            flash('Passwords do not match!', category='error')
        else:
            result = db.session.execute(sa.select(User).filter_by(email=email)).first()
            if result:
                flash('There is already an account registered with the Email!', category='error')
            else:
                newUser = User(name=name, email=email, type=UserType.ordinary, pwhash=generate_password_hash(password1))
                db.session.add(newUser)
                db.session.commit()
                login_user(newUser)
                flash('Account created!', category='success')
                return redirect(url_for('viewsBP.home'))
    return render_template('sign-up.html', user=current_user)


@authBP.route('/changepw', methods=['GET', 'POST'])
@login_required
def changePassword():
    if request.method == 'POST':
        oldPassword = request.form.get('oldPassword')
        newPassword = request.form.get('newPassword')
        user: User = db.session.get(User, current_user.id)
        if check_password_hash(user.pwhash, oldPassword):
            user.pwhash = generate_password_hash(newPassword)
            db.session.commit()
            flash('Password changed successfully!', category='success')
        else:
            flash('Password is not correct!', category='error')
        return redirect(url_for('viewsBP.home'))
    else:
        return render_template('change-password.html', user=current_user)