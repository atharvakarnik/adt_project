from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    username = "new_user"  # Replace with the desired username
    password = "password123"  # Replace with the desired password
    is_manager = False  # Set to True if this user is a manager

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print("User already exists!")
    else:
        # Create new user
        new_user = User(username=username, password_hash=generate_password_hash(password), is_manager=is_manager)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} added successfully.")
