from flask import Blueprint, request, jsonify
from schemas import UserCreate, UserLogin
from services import user_service

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = UserCreate(**request.json)
        user_id = user_service.create_user(data)
        return jsonify({"status": "success", "user_id": user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email})
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Invalid data"}), 400
    if user_service.update_user(user_id, name, email):
        return jsonify({"message": "User updated"})
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_service.delete_user(user_id):
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/search', methods=['GET'])
def search():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Missing name parameter"}), 400
    users = user_service.search_users(name)
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = UserLogin(**request.json)
        user = user_service.login_user(data)
        if user:
            return jsonify({"status": "success", "user_id": user.id})
        return jsonify({"status": "failed"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
