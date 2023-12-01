from app import create_app, db
from app.models import Employee, Department, Location, LoginCredentials

app = create_app()
with app.app_context():
    # Assume these are the values collected from the form
    emp_name = "Jane Doe"
    dept_name = "Development"
    location_name = "Headquarters"
    username = "janedoe"
    password = "strong_password123"
    is_manager = True

    # Add Department if it doesn't exist
    department = Department.query.filter_by(dept_name=dept_name).first()
    if not department:
        department = Department(dept_name=dept_name)
        db.session.add(department)

    # Add Location if it doesn't exist
    location = Location.query.filter_by(location_name=location_name).first()
    if not location:
        location = Location(location_name=location_name)
        db.session.add(location)

    # Commit new department and location to obtain IDs
    db.session.commit()

    # Check if username already exists in LoginCredentials
    if not LoginCredentials.query.filter_by(username=username).first():
        # Add new Employee
        new_employee = Employee(emp_name=emp_name, department=department, location=location)
        db.session.add(new_employee)
        db.session.flush()  # This will populate new_employee.emp_id

        # Add LoginCredentials for the new employee
        new_login_credential = LoginCredentials(username=username, password_hash=generate_password_hash(password), is_manager=is_manager, employee=new_employee)
        db.session.add(new_login_credential)
        db.session.commit()
        print(f"New employee {emp_name} with username {username} added successfully.")
    else:
        print("This username already exists.")
