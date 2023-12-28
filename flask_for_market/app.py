import sqlite3
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#database initialization
db = SQLAlchemy(app)

@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')

@app.route('/market/')
def market():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Labtop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('market.html', items=items)