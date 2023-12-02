from flask import request, jsonify, session
from .models import Employee, Department, Location, LoginCredentials, db
from werkzeug.security import generate_password_hash

@app.route('/add_user', methods=['POST'])
def add_user():
    # Check if the logged-in user is a manager
    if 'user_id' not in session or not session.get('is_manager', False):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json

    # Validate required fields
    required_fields = ['emp_name', 'dept_name', 'location_name', 'username', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing data'}), 400

    # Check if username already exists
    if LoginCredentials.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    # Add department and location if they don't exist
    department = Department.query.filter_by(dept_name=data['dept_name']).first()
    if not department:
        department = Department(dept_name=data['dept_name'])
        db.session.add(department)

    location = Location.query.filter_by(location_name=data['location_name']).first()
    if not location:
        location = Location(location_name=data['location_name'])
        db.session.add(location)

    db.session.flush()  # Flush to get the IDs of the new department and location

    # Create new employee
    new_employee = Employee(emp_name=data['emp_name'], department=department, location=location)
    db.session.add(new_employee)
    db.session.flush()  # Flush to get the ID of the new employee

    # Create login credentials for the new employee
    new_login_credential = LoginCredentials(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        is_manager=data.get('is_manager', False),
        emp_id=new_employee.emp_id
    )
    db.session.add(new_login_credential)
    db.session.commit()

    return jsonify({'message': 'Employee added successfully'}), 201
