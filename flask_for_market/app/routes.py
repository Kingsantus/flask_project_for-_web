from app import app
from flask import render_template, redirect, url_for, flash, request
from app.models import Items, Users
from app.forms import RegisterForm, LoginForm, PurchasesItemForm, SellItemForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')

@app.route('/market/', methods=['GET', 'POST'])
@login_required
def market():
    purchase_form = PurchasesItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Items.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulation you purchased {p_item_object} for ${p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, you dont't have enough money to purchase {p_item_object.name}", category='danger')
        
        sold_item = request.form.get('sold_item')
        s_item_object = Items.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulation, You sold {s_item_object.name} back to market! ${s_item_object.price}', category='success')
            else:
                flash(f'Something went wrong with selling {s_item_object.name}', category='danger')
        return redirect(url_for('market'))
    if request.method == 'GET':
        items = Items.query.filter_by(owner=None)
        owned_items = Items.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Users(username=form.username.data, email_address=form.email_address.data, password1=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')
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