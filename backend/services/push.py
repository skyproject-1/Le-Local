"""Push notification service using Firebase Cloud Messaging"""

import os
import requests


def send_push_notification(token, title, body):
    """Send push notification via FCM"""
    fcm_key = os.environ.get('FCM_SERVER_KEY', '')
    
    if not fcm_key:
        print("FCM not configured. Set FCM_SERVER_KEY in .env")
        return False
    
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            "Authorization": f"key={fcm_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": token,
            "notification": {
                "title": title,
                "body": body,
                "icon": "https://lelocal.co.uk/assets/img/lelocal-removebg-preview.png"
            },
            "web_push": {
                "fcm_options": {
                    "link": "https://lelocal.co.uk"
                }
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
        
    except Exception as e:
        print(f"Failed to send push notification: {e}")
        return False


def send_order_status_push(user_fcm_token, order_id, status):
    """Send order status update push notification"""
    status_messages = {
        'confirmed': 'Your order has been confirmed!',
        'preparing': 'Your order is being prepared...',
        'ready': 'Your order is ready!',
        'out_for_delivery': 'Your order is on its way!',
        'delivered': 'Your order has been delivered!',
        'cancelled': 'Your order has been cancelled.'
    }
    
    title = f"Le Local Order #{order_id}"
    body = status_messages.get(status, f"Order status: {status}")
    
    return send_push_notification(user_fcm_token, title, body)


def subscribe_to_topic(fcm_token, topic):
    """Subscribe a token to a topic for mass notifications"""
    fcm_key = os.environ.get('FCM_SERVER_KEY', '')
    
    if not fcm_key:
        return False
    
    try:
        url = "https://iid.googleapis.com/iid/v1:batchAdd"
        headers = {
            "Authorization": f"key={fcm_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": f"/topics/{topic}",
            "registration_tokens": [fcm_token]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
        
    except Exception as e:
        print(f"Failed to subscribe to topic: {e}")
        return False
