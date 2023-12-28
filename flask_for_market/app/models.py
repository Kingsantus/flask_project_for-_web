from app import db
#model initialization
class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=255), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Float(), nullable=False, default=0.0)
    items = db.relationship('Items', backref='owned_user', lazy=True)

    def __repr__(self):
        return f'<Users {self.id}>'


class Items(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False)
    description = db.Column(db.String(length=512), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'), )

    def __repr__(self):
        return f'<Items {self.name}>'
