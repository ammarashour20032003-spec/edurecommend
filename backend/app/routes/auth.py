from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app import db, bcrypt
from app.models.user import User
from app.models.session import Session
from app.utils.auth_helper import generate_token, decode_token
from app.utils.decorators import token_required
from app.recommender.content_fetcher import fetch_and_save_content

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password') or not data.get('full_name'):
        return jsonify({'error': 'full_name, email and password are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        full_name      = data['full_name'],
        email          = data['email'],
        password_hash  = password_hash,
        specialization = data.get('specialization'),
        level          = data.get('level')
    )

    db.session.add(user)
    db.session.commit()

    if user.specialization and user.level:
        fetch_and_save_content(user.specialization, user.level)

    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = generate_token(user.id)

    session = Session(
        user_id    = user.id,
        token      = token,
        expires_at = datetime.utcnow() + timedelta(hours=24)
    )

    user.last_login = datetime.utcnow()
    db.session.add(session)
    db.session.commit()

    return jsonify({'message': 'Login successful', 'token': token, 'user': user.to_dict()}), 200


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(user_id):
    token = request.headers['Authorization'].split()[1]

    session = Session.query.filter_by(token=token).first()
    if session:
        db.session.delete(session)
        db.session.commit()

    return jsonify({'message': 'Logged out successfully'}), 200