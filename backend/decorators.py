from functools import wraps
from flask import request, jsonify, current_app
import jwt
# TODO: Implement the jwt_required and admin_required decorators
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.split("Bearer ")[-1] if "Bearer " in auth_header else None
        if not token:
            return jsonify({"error": "Authorization token is missing!"}), 403
        try:
            payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            request.user = payload  
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    @jwt_required
    def decorated_function(*args, **kwargs):
        if request.user.get("role") != "admin":
            return jsonify({"error": "Admin access required!", "user_id": request.user.get("user_id"),"role":request.user.get("role")}), 403
        return f(*args, **kwargs)
    return decorated_function
