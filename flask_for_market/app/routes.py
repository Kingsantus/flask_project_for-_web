from app import app
from flask import render_template, redirect, url_for, flash
from app.models import Items, Users
from app.forms import RegisterForm, LoginForm
from app import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')

@app.route('/market/')
@login_required
def market():
    items = Items.query.all()
    return render_template('market.html', items=items)

@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Users(username=form.username.data, email_address=form.email_address.data, password1=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash('Usename and Password are not match! Please Try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout/')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('index'))