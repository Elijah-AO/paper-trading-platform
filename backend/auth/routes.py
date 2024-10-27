from flask import Blueprint, request, jsonify, current_app
from extensions import mongo, bcrypt
from utils import generic_error_response, create_token
from datetime import datetime
from bson import ObjectId
import jwt, os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    role = role if role else 'user'
    
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
            token = create_token(str(user["_id"]), user["role"])
            
            return jsonify({
                'message': 'Logged in successfully!',
                'token': token,
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return generic_error_response(e)

@auth_bp.route('/me', methods=['GET'])
def me():
    token = request.headers.get('Authorization').split(" ")[1]
    if not token:
        return jsonify({'error': 'Token is required'}), 400

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        user = mongo.db.users.find_one({"_id": ObjectId(payload["user_id"])})
        user['_id'] = str(user['_id'])
        print(type(user['_id']))
        user_data = {
            "id": str(user["_id"]),
            "email": user.get("email"),
            "balance": user.get("balance", 0.0),
            "role": user.get("role", "user"),
            "transactions": [str(txn) for txn in user.get("transactions", [])],
            "trades": [str(trade) for trade in user.get("trades", [])],
            "stocks": user.get("stocks", {})
        }
        return jsonify(user_data), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return generic_error_response(e)