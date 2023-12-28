from app import app
from flask import render_template, redirect, url_for, flash
from app.models import Items, Users
from app.forms import RegisterForm
from app import db

@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')

@app.route('/market/')
def market():
    items = Items.query.all()
    return render_template('market.html', items=items)

@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Users(username=form.username.data, email_address=form.email_address.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        redirect(url_for('market'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)