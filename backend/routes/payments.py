"""Payment processing routes using SumUp API"""

import os
import uuid

import requests
from flask import Blueprint, request, jsonify


bp = Blueprint('payments', __name__)

SUMUP_API_URL = "https://api.sumup.com/v0.1/checkouts"


def get_sumup_credentials():
    """Get SumUp API credentials from environment"""
    api_key = os.environ.get('SUMUP_API_KEY', '')
    merchant_code = os.environ.get('SUMUP_MERCHANT_CODE', '')
    return api_key, merchant_code


@bp.route('/create-checkout', methods=['POST'])
def create_checkout():
    """Create a new SumUp checkout for card payments"""
    data = request.json
    amount = data.get('amount')
    currency = data.get('currency', 'GBP')
    description = data.get('description', 'Le Local Order')

    api_key, merchant_code = get_sumup_credentials()
    if not api_key:
        return jsonify({'error': 'SUMUP_API_KEY not set'}), 500
    if not merchant_code:
        return jsonify({'error': 'SUMUP_MERCHANT_CODE not set'}), 500

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": float(amount),
            "currency": currency,
            "checkout_reference": str(uuid.uuid4()),
            "merchant_code": merchant_code,
            "description": description,
            "redirect_url": "https://lelocal.co.uk/payment-success",
            "hosted_checkout": {"enabled": True}
        }
        response = requests.post(SUMUP_API_URL, json=payload, headers=headers)
        
        if response.status_code != 201:
            return jsonify({'error': response.text}), 500
        
        checkout_data = response.json()
        checkout_url = checkout_data.get('hosted_checkout_url')
        
        if not checkout_url:
            checkout_id = checkout_data.get('id')
            checkout_url = f"https://checkout.sumup.com/pay/{checkout_id}"
        
        return jsonify({
            'checkout_id': checkout_data.get('id'),
            'checkout_url': checkout_url
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/wallet-topup', methods=['POST'])
def create_wallet_topup():
    """Create a SumUp checkout for wallet top-up"""
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    
    if not user_id or not amount:
        return jsonify({'error': 'Missing user_id or amount'}), 400
    
    api_key, merchant_code = get_sumup_credentials()
    if not api_key:
        return jsonify({'error': 'SUMUP_API_KEY not set'}), 500
    if not merchant_code:
        return jsonify({'error': 'SUMUP_MERCHANT_CODE not set'}), 500

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": float(amount),
            "currency": "GBP",
            "checkout_reference": f"wallet_topup_{user_id}_{uuid.uuid4().hex[:8]}",
            "merchant_code": merchant_code,
            "description": f"Wallet Top-Up - User {user_id}",
            "redirect_url": f"https://lelocal.co.uk/le-local-account.html?wallet_topup=success&user_id={user_id}&amount={amount}",
            "hosted_checkout": {"enabled": True}
        }
        response = requests.post(SUMUP_API_URL, json=payload, headers=headers)
        
        if response.status_code != 201:
            return jsonify({'error': response.text}), 500
        
        checkout_data = response.json()
        checkout_url = checkout_data.get('hosted_checkout_url')
        
        if not checkout_url:
            checkout_id = checkout_data.get('id')
            checkout_url = f"https://checkout.sumup.com/pay/{checkout_id}"
        
        return jsonify({
            'checkout_id': checkout_data.get('id'),
            'checkout_url': checkout_url,
            'amount': amount
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle SumUp payment webhook for confirmation"""
    data = request.json
    checkout_id = data.get('checkout_id')
    status = data.get('status')
    
    if status == 'PAID':
        return jsonify({'message': 'Payment received'}), 200
    
    return jsonify({'message': 'Webhook processed'}), 200


@bp.route('/check-payment/<checkout_id>', methods=['GET'])
def check_payment(checkout_id):
    """Check the status of an existing checkout"""
    api_key, _ = get_sumup_credentials()
    if not api_key:
        return jsonify({'error': 'SUMUP_API_KEY not set'}), 500

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{SUMUP_API_URL}/{checkout_id}", headers=headers)
        
        if response.status_code != 200:
            return jsonify({'error': 'Checkout not found'}), 404
        
        checkout_data = response.json()
        return jsonify({
            'id': checkout_data.get('id'),
            'status': checkout_data.get('status'),
            'amount': checkout_data.get('amount'),
            'currency': checkout_data.get('currency')
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
