from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from datetime import datetime
import os
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_CLUSTER')}/{os.getenv('MONGO_DATABASE')}?retryWrites=true&w=majority"
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

@app.route('/api/signup', methods=['POST'])
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
        }
        result = mongo.db.users.insert_one(user_data)

        return jsonify({'message': 'User created successfully!', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

@app.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = mongo.db.users.find_one({"email": email})
        if user and bcrypt.check_password_hash(user["hashed_password"], password):
            return jsonify({
                'message': 'Logged in successfully!',
                'user_id': str(user["_id"]),
                'email': user["email"],
                'role': user.get("role", "USER"),
                'balance': user.get("balance", 0.0) 
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = mongo.db.users.find()
        user_list = [{"id": str(user["_id"]), "email": user.get("email"), "balance": user.get("balance", 0.0), "role": user.get("role", "USER")} for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    try:
        stocks = mongo.db.stocks.find()
        stock_list = [{"id": str(stock["_id"]), "stock_name": stock.get("stock_name"), "stock_symbol": stock.get("stock_symbol"), "stock_price": stock.get("stock_price", 0.0)} for stock in stocks]
        return jsonify(stock_list), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
