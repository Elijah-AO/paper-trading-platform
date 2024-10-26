from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os, jwt
from bson.objectid import ObjectId
from alpaca_handler import get_assets, get_stock_data
from user.routes import user_bp
from auth.routes import auth_bp
from stock.routes import stock_bp
from transaction.routes import transaction_bp
from extensions import mongo, bcrypt

load_dotenv()

app = Flask(__name__)
CORS(app)


mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_CLUSTER')}/{os.getenv('MONGO_DATABASE')}?retryWrites=true&w=majority"
app.config["MONGO_URI"] = mongo_uri
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

mongo.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(stock_bp, url_prefix='/api/stocks')
app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == '__main__':
    app.run(debug=True)
