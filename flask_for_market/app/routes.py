from app import app
from flask import render_template
from app.models import Items

@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')

@app.route('/market/')
def market():
    items = Items.query.all()
    return render_template('market.html', items=items)