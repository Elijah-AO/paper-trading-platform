from flask import Blueprint, request, jsonify, current_app
from extensions import mongo, bcrypt
from utils import generic_error_response, get_stock_data, create_token 
from datetime import datetime, timedelta
import jwt
from bson.objectid import ObjectId

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/')
def get_transactions():
    try:
        transactions =[]
        for transaction in mongo.db.transactions.find():
            transactions.append({
                "id": str(transaction["_id"]),
                "user_id": transaction.get("user_id"),
                "type": transaction.get("type"),
                "amount": transaction.get("amount", 0.0),
                "date_created": transaction.get("date_created")
            })
        return jsonify(transactions), 200
    except Exception as e:
        return generic_error_response(e)
   
@transaction_bp.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    amount = data.get('amount', 0.0)
    user_id = data.get('user_id')

    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404

        current_balance = user.get("balance", 0.0)
        if current_balance < amount:
            return jsonify({'error': 'Insufficient funds'}), 400

        updated_balance = current_balance - amount
        
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": updated_balance}})
        
        transaction_data = {
            "user_id": user_id,
            "type": "WITHDRAWAL",
            "amount": amount,
            "date_created": datetime.now()
        }
        transaction_id = mongo.db.transactions.insert_one(transaction_data).inserted_id
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$push": {"transactions": transaction_id}})
    
        return jsonify({'message': 'Withdrawal successful!'}), 200
    except Exception as e:
        return generic_error_response(e)

@transaction_bp.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount', 0.0)

    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404

        current_balance = user.get("balance", 0.0)
        updated_balance = current_balance + amount
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": updated_balance}})
        
        transaction_data = {
            "user_id": user_id,
            "type": "DEPOSIT",
            "amount": amount,
            "date_created": datetime.now()
        }
        transaction_id = mongo.db.transactions.insert_one(transaction_data).inserted_id
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$push": {"transactions": transaction_id}})
        
        return jsonify({'message': 'Deposit successful!'}), 200
    except Exception as e:
        return generic_error_response(e)

