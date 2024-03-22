from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies, get_jwt, \
    create_access_token
from backend.app import db, app
from backend.app.models import User
from datetime import datetime, timezone, timedelta


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@app.route('/app/api/v1.0/register', methods=['POST'])
def register():
    print("here")
    username = request.json.get('username')
    password = request.json.get('password')

    if request.method == 'POST':
        if not (username or password):
            return jsonify({'message': 'Missing arguments'}), 400
        if User.query.filter_by(username=username).first() is None:
            new_user = User(username=username)
            new_user.hash_password(password)
            new_user.first_name = None
            new_user.last_name = None
            new_user.birth_date = None
            new_user.email = None
            new_user.phone_number = None
            db.session.add(new_user)
            db.session.commit()

            access_token = new_user.get_token()
            response = jsonify({'message': f'User-{new_user.username} registered successfully'})
            set_access_cookies(response, access_token)
            return response, 201
        else:
            return jsonify({'message': 'Existing user'}), 400


@app.route('/app/api/v1.0/login', methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']

    if request.method == 'POST':
        if not (username or password):
            return jsonify({'message': 'Missing arguments'}), 400
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({'message': 'Invalid username'}), 401
        else:
            if user is not None and user.verify_password(password):
                access_token = user.get_token()
                response = jsonify({'message': f'User-{user.username} authenticated successfully'})
                set_access_cookies(response, access_token)
                return response, 200
            else:
                return jsonify({'message': 'Invalid password'}), 401


@app.route('/app/api/v1.0/update', methods=['PUT'])
@jwt_required()
def update_user_information():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    data = request.json
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.birth_date = data.get('birth_date', user.birth_date)
    user.email = data.get('email', user.email)
    user.phone_number = data.get('phone_number', user.phone_number)
    db.session.commit()
    return jsonify({'message': f'Hello, {user.username}! Your data updated successfully!'}), 200
