# ⚙️ Configuration Guide

This guide will help you set up all the required environment variables for your memecoin bot.

## 🔧 Required Environment Variables

### 1. Flask Configuration
```env
SECRET_KEY=your-super-secret-key-change-this
FLASK_DEBUG=False
```

**How to generate SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

### 2. Telegram Bot Configuration
```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

**How to get Telegram Bot Token:**
1. Message @BotFather on Telegram
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the token provided

**How to get Chat ID:**
1. Message @userinfobot on Telegram
2. Copy your chat ID from the response

### 3. Solana Configuration
```env
SOLANA_PRIVATE_KEY=your-base58-private-key-here
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
```

**How to get Private Key:**
1. Export from your wallet (Phantom, Solflare, etc.)
2. Ensure it's in base58 format
3. **⚠️ Never share this key!**

### 4. Bot Trading Configuration
```env
MIN_LIQUIDITY=1000
MAX_SLIPPAGE=0.05
TRADE_AMOUNT=0.01
```

- `MIN_LIQUIDITY`: Minimum liquidity in SOL for safe trading
- `MAX_SLIPPAGE`: Maximum slippage tolerance (0.05 = 5%)
- `TRADE_AMOUNT`: Amount of SOL to trade per token

### 5. PumpFun API (Optional)
```env
PUMPFUN_API_KEY=your-api-key
PUMPFUN_SECRET=your-secret
```

## 🚀 Quick Setup

### For Local Development:
1. Create a `.env` file in the project root
2. Copy the variables above and fill in your values
3. Run `python test_deployment.py` to verify

### For Hosting Platforms:

#### Railway/Heroku:
1. Go to your app dashboard
2. Find "Environment Variables" section
3. Add each variable with its value

#### Hostinger:
1. In your hosting control panel
2. Find "Environment Variables" or "PHP Variables"
3. Add each variable

## 🔒 Security Best Practices

1. **Never commit sensitive data to Git**
   - Keep `.env` file in `.gitignore`
   - Use hosting platform's secure environment storage

2. **Use strong SECRET_KEY**
   - Generate a random 32-byte hex string
   - Change it for each deployment

3. **Secure your private key**
   - Use a dedicated wallet for bot trading
   - Never share or expose your private key
   - Consider using hardware wallets for large amounts

## 📊 Configuration Examples

### Minimal Configuration (Local Testing)
```env
SECRET_KEY=test-secret-key-change-in-production
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
SOLANA_PRIVATE_KEY=your-base58-private-key
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
```

### Production Configuration
```env
SECRET_KEY=your-32-byte-hex-secret-key-generated-securely
FLASK_DEBUG=False
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
SOLANA_PRIVATE_KEY=your-base58-private-key
SOLANA_RPC_URL=https://your-custom-rpc-endpoint.com
MIN_LIQUIDITY=2000
MAX_SLIPPAGE=0.03
TRADE_AMOUNT=0.005
PUMPFUN_API_KEY=your-api-key
PUMPFUN_SECRET=your-secret
```

## 🧪 Testing Your Configuration

Run the test script to verify your setup:

```bash
python test_deployment.py
```

This will check:
- ✅ All required modules can be imported
- ✅ Environment variables are set
- ✅ Required directories exist
- ✅ Web server can start

## 🔧 Troubleshooting

### Common Issues:

1. **"Missing environment variables"**
   - Check that all required variables are set
   - Verify variable names are correct (case-sensitive)

2. **"Invalid private key"**
   - Ensure the key is in base58 format
   - Check for extra spaces or characters

3. **"Telegram bot not responding"**
   - Verify bot token is correct
   - Check that chat ID is correct
   - Ensure bot is not blocked

4. **"RPC connection failed"**
   - Check your internet connection
   - Try a different RPC endpoint
   - Verify the URL format

## 📈 Performance Optimization

### RPC Endpoints:
- **Free**: `https://api.mainnet-beta.solana.com`
- **Better**: Use a custom RPC provider (Alchemy, QuickNode, etc.)
- **Best**: Dedicated RPC endpoint for faster transactions

### Trading Parameters:
- Start with small amounts (`TRADE_AMOUNT=0.01`)
- Use conservative slippage (`MAX_SLIPPAGE=0.05`)
- Set reasonable liquidity minimums (`MIN_LIQUIDITY=1000`)

## 🎯 Next Steps

After configuring:

1. **Test locally** with `python test_deployment.py`
2. **Deploy to hosting** following [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Monitor the dashboard** for trading activity
4. **Adjust parameters** based on performance

---

**Happy Trading! 🚀📈**