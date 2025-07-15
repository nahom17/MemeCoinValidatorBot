# PumpFun Memecoin Trading Bot

A real-time automated trading bot for PumpFun memecoins that monitors new token launches and executes trades based on safety checks and profit targets.

## Features

- 🔍 **Real-time token detection** via PumpFun WebSocket
- 🛡️ **Safety checks** for liquidity, mint authority, freeze authority, and burn status
- 💰 **Automated buying** using Jupiter DEX aggregator
- 📊 **Price monitoring** with real-time profit/loss tracking
- 🎯 **Smart selling** with configurable profit targets and stop-loss
- 📱 **Telegram alerts** for trade notifications
- 🖥️ **Web dashboard** for monitoring trades

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Solana Wallet (Required)
PRIVATE_KEY=your_base58_private_key_here

# RPC Endpoint (Required)
RPC_URL=https://api.mainnet-beta.solana.com

# Telegram Bot (Required for alerts)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Optional: Custom RPC (for better performance)
# RPC_URL=https://your-custom-rpc-endpoint.com
```

### 3. Get Your Private Key

**⚠️ IMPORTANT: Never share your private key!**

1. Export your private key from your wallet (Phantom, Solflare, etc.)
2. Make sure you have SOL for trading (recommend at least 0.1 SOL for testing)

### 4. Setup Telegram Bot (Optional)

1. Create a bot with @BotFather on Telegram
2. Get your chat ID by messaging @userinfobot
3. Add the bot token and chat ID to your `.env` file

## Usage

### Local Development

```bash
# Start the bot with web dashboard
python run.py

# Or use the deployment script
python deploy.py
```

The bot will:
1. Connect to PumpFun WebSocket
2. Monitor for new token launches
3. Perform safety checks on each token
4. Execute buy orders for safe tokens
5. Monitor prices and sell based on profit/loss targets

### Web Dashboard

Access the dashboard at `http://localhost:8080` to monitor:
- Real-time trading data
- MEV alerts and flags
- Bot status monitoring
- Profit/Loss tracking
- Active token monitoring

### Live Hosting Deployment

For 24/7 operation, deploy to hosting platforms:

#### Quick Deploy to Railway (Recommended)
1. Push your code to GitHub
2. Connect repository to [Railway](https://railway.app)
3. Set environment variables in Railway dashboard
4. Deploy automatically

#### Deploy to Hostinger
1. Upload files to your hosting directory
2. Set Python entry point to `wsgi.py`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables

#### Deploy to Heroku
```bash
heroku create your-memecoin-bot
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

**📖 See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed hosting instructions**

### Test Deployment Locally
```bash
python test_deployment.py
```

## Trading Strategy

### Buy Conditions
- ✅ Token passes all safety checks
- ✅ Sufficient liquidity (>1 SOL)
- ✅ Mint authority renounced
- ✅ Freeze authority disabled
- ✅ Tokens burned
- ✅ Reasonable supply size

### Sell Conditions
- 💰 **Take Profit**: 100% profit
- 🔻 **Stop Loss**: 30% loss
- ⏰ **Time-based**: Sell after 24 hours if no significant profit

## Safety Features

- **Risk Management**: Only trades tokens that pass comprehensive safety checks
- **Slippage Protection**: Uses Jupiter DEX with 1% slippage tolerance
- **Error Handling**: Automatic reconnection on WebSocket disconnects
- **Price Validation**: Real-time price fetching from PumpFun API

## Configuration

### Trading Parameters

Edit `bot/scheduler.py` to modify:
- Buy amount per trade (default: 0.01 SOL)
- Profit targets
- Stop-loss percentages
- Monitoring intervals

### Risk Settings

Edit `bot/risk.py` to adjust:
- Minimum liquidity requirements
- Supply size limits
- Additional safety checks

## Monitoring

### Logs
The bot provides detailed logging:
- 🚀 New token detection
- 🔍 Safety check results
- 💰 Buy/sell transactions
- 📊 Price updates
- ❌ Error messages

### Telegram Alerts
Receive notifications for:
- Successful buys
- Successful sells
- Error conditions

## Disclaimer

⚠️ **Trading cryptocurrencies involves significant risk. This bot is for educational purposes only.**

- Never invest more than you can afford to lose
- Test with small amounts first
- Monitor the bot regularly
- Be aware of market volatility and potential losses

## Troubleshooting

### Common Issues

1. **"PRIVATE_KEY not found"**
   - Check your `.env` file
   - Ensure the private key is in base58 format

2. **"WebSocket connection failed"**
   - Check your internet connection
   - The bot will automatically reconnect

3. **"Transaction failed"**
   - Ensure you have sufficient SOL
   - Check RPC endpoint connectivity

4. **"Token not found on PumpFun"**
   - Some tokens may not be immediately available
   - The bot will skip unavailable tokens

### Performance Tips

- Use a reliable RPC endpoint for better transaction success
- Monitor gas fees and adjust trading amounts accordingly
- Consider using a dedicated wallet for bot trading

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify your environment configuration
3. Test with small amounts first

## License

This project is for educational purposes. Use at your own risk.