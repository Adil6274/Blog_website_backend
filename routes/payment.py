from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import stripe
import os

payment = Blueprint('payment', __name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@payment.route('/', methods=['POST'])
@jwt_required()
def create_payment_intent():
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,  # $10.00 (example price)
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'}
        )
        return jsonify(clientSecret=payment_intent['client_secret'])
    except Exception as e:
        return jsonify(error=str(e)), 403

@payment.route('/verify', methods=['POST'])
@jwt_required()
def verify_payment():
    data = request.get_json()
    payment_intent_id = data['paymentIntentId']
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        if payment_intent['status'] == 'succeeded':
            return jsonify({'msg': 'Payment successful. Full access granted to the blog post.'})
        else:
            return jsonify({'msg': 'Payment failed or incomplete.'}), 400
    except Exception as e:
        return jsonify(error=str(e)), 403