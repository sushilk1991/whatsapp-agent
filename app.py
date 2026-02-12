#!/usr/bin/env python3
"""
WhatsApp AI Agent - Full Feature Version
Multi-product support, ordering, FAQ, and analytics
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from twilio.rest import Client
import requests
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
AI_MODEL = os.environ.get('AI_MODEL', 'gpt-4o-mini')

# Database (file-based for simplicity)
DATA_DIR = os.environ.get('DATA_DIR', '/tmp/whatsapp-agent')
os.makedirs(DATA_DIR, exist_ok=True)

# In-memory storage
conversations = {}
orders = []
products = [
    {"id": 1, "name": "Premium T-Shirt", "price": 599, "description": "Cotton, comfortable"},
    {"id": 2, "name": "Casual Hoodie", "price": 999, "description": "Warm and stylish"},
    {"id": 3, "name": "Denim Jacket", "price": 1499, "description": "Classic look"},
    {"id": 4, "name": "Running Shoes", "price": 1999, "description": "Comfortable footwear"},
]

# FAQ database
FAQS = [
    {"question": "delivery time", "answer": "🚚 We deliver within 3-5 days across India. Free delivery on orders above ₹500!"},
    {"question": "payment", "answer": "💳 We accept UPI, Cards, and Cash on Delivery!"},
    {"question": "return", "answer": "🔄 7-day return policy! Just message us with your order number."},
    {"question": "contact", "answer": "📱 Call us at +91-XXXXXXXXXX or reply here anytime!"},
]

# Business context
SYSTEM_PROMPT = """You are a helpful sales assistant for an Indian online store.
Your tone: Friendly, helpful, conversational (like a helpful shopkeeper)
Language: English (can switch to Hindi if customer uses Hindi)
Products: Fashion items (tshirts, hoodies, jackets, shoes)
Price range: ₹599 - ₹1999
Currency: Indian Rupees (₹)

Guidelines:
1. Always be polite and warm
2. Help customers find what they need
3. Provide product details when asked
4. Guide them to place orders
5. Mention ongoing offers
6. Keep responses short and friendly
7. Use emojis sparingly

Current products:
- Premium T-Shirt: ₹599
- Casual Hoodie: ₹999  
- Denim Jacket: ₹1499
- Running Shoes: ₹1999

Always end with a question to keep conversation going!"""


def load_conversations():
    """Load conversations from file"""
    try:
        with open(f"{DATA_DIR}/conversations.json", 'r') as f:
            return json.load(f)
    except:
        return {}


def save_conversations():
    """Save conversations to file"""
    with open(f"{DATA_DIR}/conversations.json", 'w') as f:
        json.dump(conversations, f)


def generate_ai_response(user_message: str, history: list = None) -> str:
    """Generate AI response"""
    if history is None:
        history = []
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add recent conversation
    for msg in history[-6:]:
        messages.append(msg)
    messages.append({"role": "user", "content": user_message})
    
    if OPENAI_API_KEY:
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": AI_MODEL,
                    "messages": messages,
                    "max_tokens": 200,
                    "temperature": 0.7
                },
                timeout=15
            )
            result = response.json()
            if 'choices' in result:
                return result['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"AI error: {e}")
    
    # Fallback: Keyword-based responses
    return fallback_response(user_message)


def fallback_response(message: str) -> str:
    """Simple keyword-based fallback"""
    msg = message.lower()
    
    if any(w in msg for w in ['hi', 'hello', 'hey', 'namaste', 'swasthyam']):
        return "Namaste! 🙏 Welcome to our store! How can I help you today? 😊"
    
    if any(w in msg for w in ['price', 'cost', 'how much', '₹', 'rupee']):
        return "Here's our price list:\n\n👕 Premium T-Shirt: ₹599\n🧥 Casual Hoodie: ₹999\n🧥 Denim Jacket: ₹1499\n👟 Running Shoes: ₹1999\n\nWhich one interests you?"
    
    if any(w in msg for w in ['buy', 'order', 'purchase', 'book']):
        return "Great choice! 🎉 To order, just tell me:\n1. Product name\n2. Quantity\n3. Your name & address\n\nWe'll confirm via WhatsApp!"
    
    if any(w in msg for w in ['delivery', 'shipping', 'deliver', 'time']):
        return "🚚 Delivery within 3-5 days across India!\n\n📦 Free delivery on orders above ₹500\n💳 COD available"
    
    if any(w in msg for w in ['return', 'exchange', 'refund']):
        return "🔄 Easy 7-day return policy! \n\nJust message us with your order number. We'll arrange pickup!"
    
    if any(w in msg for w in ['catalog', 'list', 'products', 'show']):
        return "Here's our collection:\n\n👕 Premium T-Shirt: ₹599\n🧥 Casual Hoodie: ₹999\n🧥 Denim Jacket: ₹1499\n👟 Running Shoes: ₹1999\n\nWhat would you like?"
    
    if any(w in msg for w in ['thank', 'thanks', 'dhanyawad']):
        return "You're welcome! 😊 Shop with us again soon!"
    
    if any(w in msg for w in ['help', 'support']):
        return "I'm here to help! Ask me about:\n- Our products & prices\n- Delivery time\n- Payment options\n- Returns\n\nWhat would you like to know?"
    
    return "Thanks for messaging! 😊 Tell me more about what you're looking for - I'd love to help you find the perfect product!"


def process_order(message: str, user: str) -> str:
    """Process potential order from message"""
    # Simple order detection
    msg = message.lower()
    
    # Check for quantity numbers
    numbers = re.findall(r'\d+', message)
    
    # Check for product mentions
    product_mentioned = None
    for p in products:
        if p['name'].lower() in msg:
            product_mentioned = p
            break
    
    if product_mentioned:
        qty = int(numbers[0]) if numbers else 1
        total = product_mentioned['price'] * qty
        
        order = {
            "id": len(orders) + 1,
            "user": user,
            "product": product_mentioned['name'],
            "quantity": qty,
            "total": total,
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        }
        orders.append(order)
        
        return f"📝 Order Received!\n\nProduct: {product_mentioned['name']}\nQuantity: {qty}\nTotal: ₹{total}\n\nWe'll confirm in 2 minutes! 🙏"
    
    return None


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        if not incoming_msg:
            return jsonify({'status': 'ok'})
        
        logger.info(f"Message from {from_number}: {incoming_msg}")
        
        # Load/save conversations
        conversations = load_conversations()
        
        if from_number not in conversations:
            conversations[from_number] = []
        
        history = conversations[from_number]
        
        # Check for order
        order_response = process_order(incoming_msg, from_number)
        if order_response:
            response_text = order_response
        else:
            # Generate AI response
            response_text = generate_ai_response(incoming_msg, history)
        
        # Save to history
        history.append({"role": "user", "content": incoming_msg})
        history.append({"role": "assistant", "content": response_text})
        
        # Keep last 20 messages
        if len(history) > 20:
            history = history[-20:]
        
        conversations[from_number] = history
        save_conversations()
        
        # Send via Twilio
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER:
            try:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=response_text,
                    from_=TWILIO_PHONE_NUMBER,
                    to=from_number
                )
            except Exception as e:
                logger.error(f"Twilio error: {e}")
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    conversations = load_conversations()
    return jsonify({
        'status': 'healthy',
        'time': datetime.now().isoformat(),
        'users': len(conversations),
        'orders': len(orders)
    })


@app.route('/products', methods=['GET'])
def get_products():
    """Get product list"""
    return jsonify({
        'products': products,
        'count': len(products)
    })


@app.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    return jsonify({
        'orders': orders,
        'count': len(orders)
    })


@app.route('/test', methods=['GET'])
def test_ai():
    """Test AI response"""
    test_msg = "Hi, what products do you have?"
    response = generate_ai_response(test_msg, [])
    return jsonify({
        'input': test_msg,
        'response': response
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting WhatsApp Agent on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
