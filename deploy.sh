#!/bin/bash
# Deploy script for WhatsApp AI Agent

echo "🤖 WhatsApp AI Agent Deployment"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check environment variables
echo "⚙️  Checking configuration..."
if [ -z "$TWILIO_ACCOUNT_SID" ]; then
    echo "⚠️  TWILIO_ACCOUNT_SID not set"
fi

# Start the app
echo "🚀 Starting server..."
echo "   Webhook URL: https://your-app.onrender.com/webhook"
echo "   Health check: https://your-app.onrender.com/health"
echo ""
echo "Press Ctrl+C to stop"

python3 app.py
