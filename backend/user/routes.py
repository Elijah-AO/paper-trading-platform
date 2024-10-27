from decorators import jwt_required, admin_required
from flask import Blueprint, request, jsonify, current_app
from extensions import mongo, bcrypt
from utils import generic_error_response, get_stock_data, create_token, get_stocks_data 
from datetime import datetime, timedelta
import jwt
from bson.objectid import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    try:
        users = mongo.db.users.find()
        user_list = [{"id": str(user["_id"]), "email": user.get("email"), "balance": user.get("balance", 0.0), "role": user.get("role", "USER")} for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return generic_error_response(e)

@user_bp.route('/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({'error': 'User not found'}), 404

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

    except Exception as e:
        return generic_error_response(e)
 
@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({'message': 'User deleted successfully!'}), 200

@user_bp.route('/dashboard', methods=['GET'])
def get_user_dashboard():
    token = request.headers.get('Authorization').split(" ")[1]

    try:
        payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        user_id = payload['user_id']

        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_data = {
            'balance': user.get('balance', 0.0),
            'stocks': []
        }

        user_stocks = user.get('stocks', {})
        
        # Get list of stock symbols
        stock_symbols = []
        stock_data_map = {}

        for _id, quantity in user_stocks.items():
            stock = mongo.db.stocks.find_one({"_id": ObjectId(_id)})
            if stock:
                stock_symbols.append(stock['symbol'])
                stock_data_map[stock['symbol']] = {
                    "_id": _id,
                    "name": stock.get("name", "Unknown"),
                    "quantity": quantity
                }

        # Fetch the latest stock data for these symbols
        if stock_symbols:
            latest_prices = get_stocks_data(stock_symbols)

            for price_data in latest_prices:
                symbol = price_data['symbol']
                if symbol in stock_data_map:
                    stock_data_map[symbol].update({
                        "latest_price": price_data['price'],
                        "timestamp": price_data['timestamp']
                    })

        # Append all stock data to user_data['stocks']
        user_data['stocks'] = list(stock_data_map.values())

        return jsonify(user_data), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except KeyError:
        return jsonify({'error': 'Invalid token structure: user_id missing'}), 400