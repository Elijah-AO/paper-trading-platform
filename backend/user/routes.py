from flask import Blueprint, request, jsonify, current_app
from extensions import mongo, bcrypt
from utils import generic_error_response, get_stock_data, create_token 
from datetime import datetime, timedelta
import jwt
from bson.objectid import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
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
            "role": user.get("role", "USER"),
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

