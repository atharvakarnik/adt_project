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
    
    # Enforcing constraints
    @validates('emp_name')
    def validate_emp_name(self, key, emp_name):
        if not emp_name:
            raise ValueError("Employee name must not be empty")
        return emp_name
    
    @validates('scheduled_hrs')
    def validate_scheduled_hrs(self, key, scheduled_hrs):
        if scheduled_hrs is not None and not (0 <= scheduled_hrs <= 24):
            raise ValueError("scheduled_hrs must be between 0 and 24")
        return scheduled_hrs

class Department(db.Model):
    __tablename__ = 'departments'
    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_name = db.Column(db.String(255), nullable=False)
    # Relationship to Attendance
    attendances = db.relationship('Attendance', backref='department', lazy=True)

    # Enforcing constraints
    def validate_dept_name(self, key, dept_name):
        if not dept_name:
            raise ValueError("Department name must not be empty")
        return dept_name

class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(255), nullable=False)
    # Relationship to Attendance
    attendances = db.relationship('Attendance', backref='location', lazy=True)

    # Enforcing constraints
    @validates('location_name')
    def validate_location_name(self, key, location_name):
        if not location_name:
            raise ValueError("Location name must not be empty")
        return location_name

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

    # Enforcing constraints

    @validates('clock_in', 'clock_out')
    def validate_clock_times(self, key, time):
        if key == 'clock_out' and self.clock_in and time:
            if time < self.clock_in:
                raise ValueError("Clock out time must be after clock in time")
        return time
    
    @validates('status')
    def validate_status(self, key, status):
        if status not in ['Approved', 'Unapproved']:
            raise ValueError("Status must be either 'Approved' or 'Unapproved'")
        return status

class LoginCredentials(db.Model):
    __tablename__ = 'login_credentials'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_manager = db.Column(db.Boolean, nullable=False, default=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('employees.emp_id'), nullable=False, unique=True)
