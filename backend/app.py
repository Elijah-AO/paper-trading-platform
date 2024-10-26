from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from datetime import datetime
import os, jwt
from bson.objectid import ObjectId
from alpaca_handler import get_assets

load_dotenv()

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_CLUSTER')}/{os.getenv('MONGO_DATABASE')}?retryWrites=true&w=majority"
app.config["MONGO_URI"] = mongo_uri
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
mongo = PyMongo(app)

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config["JWT_SECRET_KEY"], algorithm="HS256")
    return token    

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
            token = create_token(str(user["_id"]))
            
            return jsonify({
                'message': 'Logged in successfully!',
                'token': token,
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

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_data = {
            "id": str(user["_id"]),
            "email": user.get("email"),
            "balance": user.get("balance", 0.0),
            "role": user.get("role", "USER")
        }
        return jsonify(user_data), 200

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


def populate_stocks():
    stocks = get_assets()
    for i, stock in enumerate(stocks):
        if i % 1000 == 0:
            print(f"Processing stock {i} of {len(stocks)}")
        existing_stock = mongo.db.stocks.find_one({"alpaca_id": stock.id})
        if not existing_stock:
            stock_data = {
                "alpaca_id": stock.id,
                "name": stock.name,
                "symbol": stock.symbol,
                "price": 0.0,
                "date_created": datetime.now(), 
                "date_updated": datetime.now(), 
            }
            mongo.db.stocks.insert_one(stock_data)

@app.route('/api/search', methods=['GET'])
def search_stocks():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    results = mongo.db.stocks.find({
        "$or": [
            {"symbol": {"$regex": query, "$options": "i"}},
            {"name": {"$regex": query, "$options": "i"}}
        ]
    })

    stock_list = [{"id": str(stock["_id"]), "symbol": stock["symbol"], "name": stock["name"]} for stock in results]
    return jsonify(stock_list), 200

if __name__ == '__main__':
    app.run(debug=True)
