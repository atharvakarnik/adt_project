from flask import request, jsonify
from .models import User, db
from werkzeug.security import generate_password_hash

@app.route('/add_user', methods=['POST'])
def add_user():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        return jsonify({'error': 'Missing data'}), 400

    # Assuming you have a way to authenticate and identify the manager
    if not current_user.is_manager:  # Replace with your actual authentication logic
        return jsonify({'error': 'Unauthorized'}), 403

    username = request.json['username']
    password = request.json['password']
    is_manager = request.json.get('is_manager', False)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    new_user = User(username=username, password_hash=generate_password_hash(password), is_manager=is_manager)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201
