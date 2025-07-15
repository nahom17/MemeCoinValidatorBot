#!/usr/bin/env python3
"""
Deployment script for running the memecoin bot with web dashboard
"""
import os
import sys
import threading
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_bot():
    """Run the trading bot in background"""
    try:
        logger.info("Starting trading bot...")
        from bot.scheduler import start_scheduler
        from bot.scanner import run_scanner, handle_token_callback

        # Start scheduler
        start_scheduler()

        # Start scanner
        run_scanner(handle_token_callback)

    except Exception as e:
        logger.error(f"Bot error: {e}")

def run_web_server():
    """Run the Flask web server"""
    try:
        logger.info("Starting web server...")
        from dashboard.app import app

        port = int(os.environ.get('PORT', 8080))
        app.run(host='0.0.0.0', port=port, debug=False)

    except Exception as e:
        logger.error(f"Web server error: {e}")

def main():
    """Main deployment function"""
    logger.info("🚀 Starting Memecoin Bot Deployment")

    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    logger.info("✅ Bot started in background")
    logger.info("🌐 Starting web dashboard...")

    # Run web server in main thread
    run_web_server()

if __name__ == "__main__":
    main()