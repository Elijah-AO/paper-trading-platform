from flask import Blueprint, request, jsonify
from extensions import mongo, bcrypt
from utils import generic_error_response
from datetime import datetime
import jwt, os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = mongo.db.users.find_one({"email": email})
    if user:
        return jsonify({'error': 'Email already exists'}), 400

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_data = {
            "email": email,
            "hashed_password": hashed_password,
            "role": role,
            "balance": 0.0,
            "date_created": datetime.now(), 
            "date_updated": datetime.now(),
            "trades": [],
            "transactions": [],
            "stocks": {}
        }
        result = mongo.db.users.insert_one(user_data)        

        return jsonify({'message': 'User created successfully!', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return generic_error_response(e)

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = mongo.db.users.find_one({"email": email})
        if user and bcrypt.check_password_hash(user["hashed_password"], password):
            token = create_token(str(user["_id"]))
            
            return jsonify({
                'message': 'Logged in successfully!',
                'token': token,
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return generic_error_response(e)