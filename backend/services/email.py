"""Email notification service for order confirmations"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_order_email(to_email, order_details):
    """Send order confirmation email"""
    smtp_host = os.environ.get('SMTP_HOST', '')
    smtp_port = os.environ.get('SMTP_PORT', '587')
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    from_email = os.environ.get('FROM_EMAIL', smtp_user)
    
    if not all([smtp_host, smtp_user, smtp_password]):
        print("Email not configured. Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD in .env")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f"Order Confirmation - Le Local #{order_details.get('order_id', 'N/A')}"
        
        items_html = ""
        for item in order_details.get('items', []):
            items_html += f"<li>{item.get('qty', 1)}x {item.get('name')} - £{item.get('price', 0):.2f}</li>"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h2 style="color: #E8641A;">Le Local Off Licence & Grocery</h2>
                <h3>Order Confirmed!</h3>
                <p>Thank you for your order, <strong>{order_details.get('customer_name')}</strong>!</p>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h4>Order Details</h4>
                    <p><strong>Order ID:</strong> #{order_details.get('order_id')}</p>
                    <p><strong>Delivery Address:</strong><br>{order_details.get('delivery_address')}</p>
                    <p><strong>Payment Method:</strong> Card Payment</p>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h4>Items Ordered</h4>
                    <ul>{items_html}</ul>
                </div>
                
                <div style="text-align: right; font-size: 18px; margin-top: 15px;">
                    <strong>Total: £{order_details.get('total', 0):.2f}</strong>
                </div>
                
                <p style="margin-top: 20px; color: #666;">
                    Your order will be delivered to your address. We'll notify you when it's on the way!
                </p>
                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    Le Local Off Licence & Grocery, Leicester<br>
                    Questions? Contact us at info@lelocal.co.uk
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(smtp_host, int(smtp_port))
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_status_email(to_email, order_id, status):
    """Send order status update email"""
    status_messages = {
        'confirmed': 'Your order has been confirmed and is being prepared.',
        'preparing': 'Your order is now being prepared by our team.',
        'ready': 'Your order is ready for collection/delivery.',
        'out_for_delivery': 'Your order is on its way!',
        'delivered': 'Your order has been delivered. Thank you!',
        'cancelled': 'Your order has been cancelled.'
    }
    
    smtp_host = os.environ.get('SMTP_HOST', '')
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    from_email = os.environ.get('FROM_EMAIL', smtp_user)
    
    if not all([smtp_host, smtp_user, smtp_password]):
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f"Order Update - Le Local #{order_id}"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h2 style="color: #E8641A;">Le Local Off Licence & Grocery</h2>
                <h3>Order Update</h3>
                <p>Your order <strong>#{order_id}</strong> status has been updated:</p>
                <div style="background: #E8641A; color: white; padding: 15px; border-radius: 8px; margin: 15px 0; text-align: center; font-size: 18px;">
                    <strong>{status.upper()}</strong>
                </div>
                <p>{status_messages.get(status, 'Your order status has been updated.')}</p>
                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    Le Local Off Licence & Grocery, Leicester
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(smtp_host, int(smtp_port or '587'))
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Failed to send status email: {e}")
        return False
