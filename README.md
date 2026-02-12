# WhatsApp AI Agent 🤖📱

AI-powered WhatsApp assistant for Indian SMBs. Never miss a customer again.

## Why This?

- **24/7 Availability** - AI never sleeps, never takes leave
- **Cheaper than staff** - ₹999/mo vs ₹15,000+/mo for human
- **Instant responses** - Customers get answers in seconds
- **Multi-language** - Works in English, Hindi, and more
- **Order taking** - Automatically captures orders

## Features

### Core
- 🤖 AI-powered auto-reply
- 📦 Product catalog management  
- 🛒 Order capture
- 📊 Basic analytics
- 🔄 Conversation memory

### Coming Soon
- 📅 Appointment booking
- 💳 Payment integration (UPI)
- 📈 Advanced analytics
- 🌐 Multi-language (Tamil, Telugu, etc.)

## Quick Start

### 1. Get Twilio Account
1. Sign up at [twilio.com](https://twilio.com)
2. Get WhatsApp Business API access
3. Note: Account SID, Auth Token, and WhatsApp number

### 2. Deploy

**Option A: Render (Free)**
```bash
# Click Deploy button at render.com
# Connect your GitHub
# Set environment variables
```

**Option B: Railway**
```bash
railway init
railway up
```

**Option C: Local**
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python app.py
```

### 3. Configure Webhook

Set your Twilio WhatsApp webhook to:
```
https://your-app.onrender.com/webhook
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Yes | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Yes | Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Yes | Twilio WhatsApp number |
| `OPENAI_API_KEY` | No | OpenAI key for smarter AI |
| `AI_MODEL` | No | Model to use (default: gpt-4o-mini) |

## Pricing Plans

| Plan | Price | Features |
|------|-------|----------|
| **Free** | ₹0 | 50 messages, basic responses |
| **Pro** | ₹999/mo | Unlimited messages, 5 products, analytics |
| **Business** | ₹2999/mo | Unlimited everything, custom training |

## API Endpoints

- `GET /health` - Health check
- `GET /products` - List products
- `GET /orders` - List orders
- `POST /webhook` - WhatsApp webhook

## Demo

Send a WhatsApp message to the deployed number to try it out!

## Tech Stack

- Python + Flask
- Twilio WhatsApp API
- OpenAI (optional)
- SQLite (file-based storage)

## License

MIT

---

Made in India 🇮🇳
