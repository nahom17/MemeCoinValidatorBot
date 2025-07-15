# 🚀 Memecoin Bot Deployment Guide

This guide will help you deploy your memecoin bot to live hosting services like Hostinger, Heroku, Railway, or any other Python hosting platform.

## 📋 Prerequisites

1. **Python 3.11+** installed on your hosting platform
2. **Git** for version control
3. **Environment variables** configured (see Configuration section)

## 🏗️ Deployment Options

### Option 1: Hostinger (Shared Hosting)

1. **Upload Files**
   - Upload all project files to your Hostinger hosting directory
   - Ensure `wsgi.py` is in the root directory

2. **Configure Python**
   - In Hostinger control panel, set Python version to 3.11
   - Set the entry point to `wsgi.py`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   - Add your configuration in Hostinger's environment variables section
   - See Configuration section below

### Option 2: Railway (Recommended)

1. **Connect Repository**
   - Connect your GitHub repository to Railway
   - Railway will automatically detect the Python app

2. **Configure Environment Variables**
   - Add all required environment variables in Railway dashboard

3. **Deploy**
   - Railway will automatically deploy using the `Procfile`

### Option 3: Heroku

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-memecoin-bot
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set TELEGRAM_BOT_TOKEN=your-bot-token
   # Add all other required variables
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

## ⚙️ Configuration

### Required Environment Variables

Create a `.env` file or set these in your hosting platform:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this
FLASK_DEBUG=False

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Solana Configuration
SOLANA_PRIVATE_KEY=your-private-key
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# Bot Configuration
MIN_LIQUIDITY=1000
MAX_SLIPPAGE=0.05
TRADE_AMOUNT=0.01

# PumpFun API
PUMPFUN_API_KEY=your-api-key
PUMPFUN_SECRET=your-secret
```

### Optional Environment Variables

```env
# Database
DATABASE_URL=sqlite:///trades.db

# Logging
LOG_LEVEL=INFO

# Web Dashboard
PORT=8080
```

## 🚀 Quick Deployment Steps

### For Hostinger:

1. **Upload Files**
   ```bash
   # Upload all files to your hosting directory
   # Ensure wsgi.py is in the root
   ```

2. **Set Python Entry Point**
   - In Hostinger control panel, set entry point to: `wsgi.py`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   - Add environment variables in Hostinger dashboard

### For Railway/Heroku:

1. **Push to Git**
   ```bash
   git add .
   git commit -m "Deploy memecoin bot"
   git push origin main
   ```

2. **Connect to Platform**
   - Connect your repository to Railway/Heroku

3. **Set Environment Variables**
   - Add all required variables in platform dashboard

## 🌐 Accessing Your Dashboard

Once deployed, you can access your dashboard at:

- **Hostinger**: `https://yourdomain.com`
- **Railway**: `https://your-app-name.railway.app`
- **Heroku**: `https://your-app-name.herokuapp.com`

## 📊 Dashboard Features

The web dashboard provides:

- **Real-time trading data**
- **MEV alerts and flags**
- **Bot status monitoring**
- **Profit/Loss tracking**
- **Active token monitoring**

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility

2. **Environment Variables**
   - Verify all required variables are set
   - Check for typos in variable names

3. **Database Issues**
   - Ensure database files are writable
   - Check file permissions

4. **WebSocket Connection**
   - Some hosting providers block WebSocket connections
   - The bot will automatically fall back to polling mode

### Logs and Debugging:

- Check hosting platform logs for errors
- Use the `/health` endpoint to verify the app is running
- Monitor the dashboard for real-time status

## 🔒 Security Considerations

1. **Environment Variables**
   - Never commit sensitive data to Git
   - Use hosting platform's secure environment variable storage

2. **Private Keys**
   - Store private keys securely
   - Use environment variables for all sensitive data

3. **Access Control**
   - Consider adding authentication to the dashboard
   - Use HTTPS in production

## 📈 Monitoring

The dashboard automatically updates every 5 seconds and shows:

- **Bot Status**: Running/Error/Connecting
- **Total Trades**: Number of completed trades
- **MEV Flags**: Number of suspicious activities detected
- **Active Tokens**: Currently monitored tokens
- **P&L**: Profit and Loss tracking

## 🆘 Support

If you encounter issues:

1. Check the hosting platform logs
2. Verify all environment variables are set
3. Test locally first with `python deploy.py`
4. Ensure all dependencies are compatible

## 🎯 Next Steps

After successful deployment:

1. **Monitor the dashboard** for trading activity
2. **Configure Telegram alerts** for notifications
3. **Adjust trading parameters** based on performance
4. **Set up monitoring** for 24/7 operation

---

**Happy Trading! 🚀📈**