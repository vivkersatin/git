from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
