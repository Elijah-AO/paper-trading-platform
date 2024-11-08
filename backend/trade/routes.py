from flask import Blueprint, request, jsonify, current_app
from extensions import mongo, bcrypt
from utils import generic_error_response, get_stock_data, create_token 
from datetime import datetime, timedelta
import jwt
from bson.objectid import ObjectId

trade_bp = Blueprint('trade', __name__)

@trade_bp.route('/', methods=['GET'])
def get_trades():
    try:
        trades = mongo.db.trades.find()
        trade_list = [
            {
                "id": str(trade["_id"]),
                "user_id": str(trade["user_id"]),
                "stock_id": str(trade["stock_id"]),
                "type": trade["type"],
                "quantity": trade["quantity"],
                "amount": trade["amount"],
                "date_created": trade["date_created"].isoformat() if trade.get("date_created") else None
            }
            for trade in trades
        ]
        return jsonify(trade_list), 200
    except Exception as e:
        return generic_error_response(e)

@trade_bp.route('/buy', methods=['POST'])
def buy_stock():
    data = request.get_json()
    user_id = data.get('user_id')
    stock_id = data.get('stock_id')
    quantity = data.get('quantity', 0)
    
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        stock = mongo.db.stocks.find_one({"_id": ObjectId(stock_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        if not stock:
            return jsonify({'error': 'Stock not found'}), 404

        stock_price = stock.get("price", 0.0)
        total_cost = stock_price * quantity
        user_balance = user.get("balance", 0.0)

        if user_balance < total_cost:
            return jsonify({'error': 'Insufficient funds'}), 400

        updated_balance = user_balance - total_cost
        updated_quantity = user["stocks"].get(stock_id, 0.0) + quantity
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": updated_balance, f"stocks.{stock_id}": updated_quantity}})
        
        trade_data = {
            "user_id": user_id,
            "stock_id": stock_id,
            "type": "BUY",
            "quantity": quantity,
            "amount": total_cost,
            "date_created": datetime.now()
        }
        trade_id = mongo.db.trades.insert_one(trade_data).inserted_id
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$push": {"trades": trade_id}})

        return jsonify({
            'message': 'Sale successful!',
            'quantity_bought': quantity,
            'symbol': stock.get("symbol"),
            'price': stock_price,
            'final_balance': updated_balance,
            'final_quantity': updated_quantity
        }), 200
    except Exception as e:
        return generic_error_response(e)
    
@trade_bp.route('/sell', methods=['POST'])
def sell_stock():
    data = request.get_json()
    user_id = data.get('user_id')
    stock_id = data.get('stock_id')
    quantity = data.get('quantity', 0)
    
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        stock = mongo.db.stocks.find_one({"_id": ObjectId(stock_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        if not stock:
            return jsonify({'error': 'Stock not found'}), 404
        
        quantity_owned = user["stocks"].get(stock_id, 0.0)
        if quantity_owned < quantity:
            return jsonify({'error': 'Insufficient quantity'}), 400

        # TODO: Refactor into helper function
        stock_data = get_stock_data(stock['symbol'])
        updated_stock = {
                "price": stock_data['price'],  
                "date_updated": datetime.now(),
            }

        mongo.db.stocks.update_one({"_id": ObjectId(stock_id)}, {"$set": updated_stock})
        stock.update(updated_stock)

        stock_price = stock.get("price", 0.0)
        total_cost = stock_price * quantity
        user_balance = user.get("balance", 0.0)

        updated_balance = user_balance + total_cost
        updated_quantity = user["stocks"].get(stock_id, 0.0) - quantity
        
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": updated_balance, f"stocks.{stock_id}": updated_quantity}})
        if updated_quantity == 0:
            mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$unset": {f"stocks.{stock_id}": ""}})
            
        trade_data = {
            "user_id": user_id,
            "stock_id": stock_id,
            "type": "SELL",
            "quantity": quantity,
            "amount": total_cost,
            "date_created": datetime.now(),
        }
        trade_id = mongo.db.trades.insert_one(trade_data).inserted_id
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$push": {"trades": trade_id}})
        
        return jsonify({
            'message': 'Sale successful!',
            'quantity': quantity,
            'symbol': stock.get("symbol"),
            'price': stock_price,
            'final_balance': updated_balance,
            'final_quantity': updated_quantity,
        }), 200
        
    except Exception as e:
        return generic_error_response(e)
