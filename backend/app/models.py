from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    is_manager = db.Column(db.Boolean, default=False)

    # Relationship with Timesheet
    timesheets = db.relationship('Timesheet', backref='user', lazy=True)

class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clock_in_time = db.Column(db.DateTime, nullable=False)
    clock_out_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Add other fields as necessary