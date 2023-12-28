import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#initializing app to accept dictionary
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'market.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#database initialization
db = SQLAlchemy(app)

#model initialization
class Items(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False)
    description = db.Column(db.String(length=512), nullable=False, unique=True)

    def __repr__(self):
        return f'<Items {self.name}>'
    

@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')

@app.route('/market/')
def market():
    items = Items.query.all()
    return render_template('market.html', items=items)