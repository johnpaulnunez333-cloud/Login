from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)

users = []

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing fields."}), 400

    existing_user = next((u for u in users if u["email"] == email), None)
    if existing_user:
        return jsonify({"success": False, "message": "Email already registered."}), 409

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users.append({"username": username, "email": email, "password_hash": password_hash})

    return jsonify({"success": True, "message": "Account Created."}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing fields."}), 400

    user = next((u for u in users if u["email"] == email), None)

    if not user:
        return jsonify({"success": False, "message": "Email not found."}), 404

    if user["username"] != username:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
        return jsonify({"success": False, "message": "Incorrect password."}), 401

    return jsonify({"success": True, "message": "Login successful.", "username": user["username"]}), 200

@app.route("/api/users", methods=["GET"])
def get_users():
    safe_users = [{"username": u["username"], "email": u["email"]} for u in users]
    return jsonify({"users": safe_users}), 200

@app.route("/")
def index():
    return jsonify({"message": "Server is running!"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)

