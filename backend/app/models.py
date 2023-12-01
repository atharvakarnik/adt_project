from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_name = db.Column(db.String(255), nullable=False)
    scheduled_hrs = db.Column(db.Integer, nullable=True)
    # Relationship to Attendance and LoginCredentials
    attendances = db.relationship('Attendance', backref='employee', lazy=True)
    login_credential = db.relationship('LoginCredentials', backref='employee', uselist=False, lazy=True)

class Department(db.Model):
    __tablename__ = 'departments'
    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_name = db.Column(db.String(255), nullable=False)
    # Relationship to Attendance
    attendances = db.relationship('Attendance', backref='department', lazy=True)

class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(255), nullable=False)
    # Relationship to Attendance
    attendances = db.relationship('Attendance', backref='location', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    clock_in = db.Column(db.Time, nullable=True)
    clock_out = db.Column(db.Time, nullable=True)
    break_duration = db.Column(db.Time, nullable=True)
    total_hrs = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(20), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('employees.emp_id'), nullable=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.dept_id'), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=True)

class LoginCredentials(db.Model):
    __tablename__ = 'login_credentials'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_manager = db.Column(db.Boolean, nullable=False, default=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('employees.emp_id'), nullable=False, unique=True)
