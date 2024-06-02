from flask import Blueprint, request, jsonify
from app import db
from models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

users = Blueprint('users', __name__)

@users.route('/subscription', methods=['PUT'])
@jwt_required()
def update_subscription():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    data = request.get_json()
    user.subscription = data['subscription']
    db.session.commit()
    return jsonify({'msg': 'Subscription updated successfully'})