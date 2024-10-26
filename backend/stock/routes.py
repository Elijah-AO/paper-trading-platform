from flask import Blueprint, request, jsonify
from extensions import mongo
from bson.objectid import ObjectId
from alpaca_handler import get_stock_data
from utils import generic_error_response, get_assets
from datetime import datetime, timedelta
stock_bp = Blueprint('stock_bp', __name__)

@stock_bp.route('/', methods=['GET'])
def get_stocks():
    try:
        stocks = mongo.db.stocks.find()
        stock_list = [{"id": str(stock["_id"]), "stock_name": stock.get("stock_name"), "stock_symbol": stock.get("stock_symbol"), "stock_price": stock.get("stock_price", 0.0)} for stock in stocks]
        return jsonify(stock_list), 200
    except Exception as e:
        return generic_error_response(e)

@stock_bp.route('/<stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    stock = mongo.db.stocks.find_one({"_id": ObjectId(stock_id)})
    if not stock:
        return jsonify({'error': 'Stock not found'}), 404
    
    mongo.db.stocks.delete_one({"_id": ObjectId(stock_id)})
    return jsonify({'message': 'Stock deleted successfully!'}), 200

@stock_bp.route('/stocks', methods=['POST'])
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

    return jsonify({'message': 'Stocks populated successfully!'}), 201


@stock_bp.route('/<stock_id>', methods=['GET'])
def get_stock_by_id(stock_id):
    try:
        stock = mongo.db.stocks.find_one({"_id": ObjectId(stock_id)})

        if not stock:
            return jsonify({'error': 'Stock not found'}), 404

        last_updated = stock.get("date_updated")
        was_updated = False
        
        if not last_updated or (datetime.now() - last_updated) > timedelta(minutes=1):
            stock_data = get_stock_data(stock['symbol'])
            updated_stock = {
                "price": stock_data['price'],  
                "date_updated": datetime.now(),
            }

            mongo.db.stocks.update_one({"_id": ObjectId(stock_id)}, {"$set": updated_stock})
            stock.update(updated_stock)
            was_updated = True

        stock_data_response = {
            "id": str(stock["_id"]),
            "name": stock.get("name"),
            "symbol": stock.get("symbol"),
            "price": stock.get("price", 0.0),
            "date_updated": stock.get("date_updated"),
            "stock_data": stock.get("stock_data"),
            "was_updated": was_updated
        }
        
        return jsonify(stock_data_response), 200

    except Exception as e:
        return generic_error_response(e)
    
    
# TODO: Add pagination and limit to the search endpoint
@stock_bp.route('/search', methods=['GET'])
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
