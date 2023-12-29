from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#model initialization
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Float(), nullable=False, default=0.0)
    items = db.relationship('Items', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[:-3]}'
        else:
            return f'${self.budget}'

    @property
    def password1(self):
        return self.password1
    
    @password1.setter
    def password1(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


class Items(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False)
    description = db.Column(db.String(length=512), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'), )

    def __repr__(self):
        return f'<Items {self.name}>'
