# bot/scheduler.py
import random
import time
import sqlite3
import os
from bot.risk import is_token_safe
from bot.buyer import buy_token
from bot.seller import should_sell, sell_token
from bot.alert import send_alert
from bot.price_tracker import fetch_token_price, calculate_profit

trades = {}

def save_trade_to_db(symbol, status, buy_price, current_price, pnl):
    """Save trade to database for dashboard display"""
    try:
        # Ensure db directory exists
        os.makedirs("db", exist_ok=True)

        conn = sqlite3.connect("db/trades.db")
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                symbol TEXT,
                status TEXT,
                buy_price REAL,
                current_price REAL,
                pnl REAL,
                time TEXT
            )
        """)

        # Insert trade
        cursor.execute("""
            INSERT INTO trades (symbol, status, buy_price, current_price, pnl, time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (symbol, status, buy_price, current_price, pnl, time.strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()
        print(f"💾 Saved trade to database: {symbol}")

    except Exception as e:
        print(f"❌ Error saving trade to database: {e}")

def handle_token_callback(token):
    token_id = token.get("mint") or token.get("address")
    symbol = token.get("symbol", "UnnamedToken")[:20]

    if not token_id:
        print("❌ No mint address found in token data.")
        return

    print(f"🔍 Checking token: {symbol} ({token_id})")

    if token_id in trades:
        print(f"⏩ Already bought {symbol}, skipping...")
        return

    # Enhanced risk checking
    if not is_token_safe(token):
        print(f"⚠️ {symbol} failed safety checks.")
        return

    # Real trading execution
    print(f"🚀 Attempting to buy {symbol}...")
    if buy_token(token):
        # Get real buy price from the transaction
        current_price = fetch_token_price(token)
        if current_price > 0:
            trades[token_id] = {
                "buy_price": current_price,
                "token": token,
                "buy_time": time.time()
            }
            print(f"✅ Bought {symbol} at {current_price} SOL")
            send_alert(f"✅ Bought {symbol} at {current_price} SOL")

            # Save to database
            save_trade_to_db(symbol, "active", current_price, current_price, 0.0)
        else:
            print(f"⚠️ Could not determine buy price for {symbol}")
    else:
        print(f"❌ Failed to buy {symbol}")


def monitor_trades():
    """Monitor existing trades for profit/loss conditions"""
    while True:
        try:
            for token_id, trade_data in list(trades.items()):
                token = trade_data["token"]
                buy_price = trade_data["buy_price"]
                symbol = token.get("symbol", "Unknown")

                # Get current price
                current_price = fetch_token_price(token)
                if current_price <= 0:
                    continue

                # Calculate profit
                profit_percentage = calculate_profit(buy_price, current_price)

                # Update database with current price
                save_trade_to_db(symbol, "active", buy_price, current_price, profit_percentage)

                # Check if we should sell
                sell_reason = should_sell(token, buy_price, current_price)

                if sell_reason:
                    print(f"💸 {symbol}: {sell_reason} - Selling...")
                    if sell_token(token):
                        print(f"✅ Sold {symbol} at {current_price} SOL")
                        send_alert(f"✅ Sold {symbol} at {current_price} SOL - {sell_reason}")

                        # Update database with sold status
                        save_trade_to_db(symbol, "sold", buy_price, current_price, profit_percentage)

                        del trades[token_id]
                    else:
                        print(f"❌ Failed to sell {symbol}")
                else:
                    print(f"📊 {symbol}: {profit_percentage}% profit/loss")

            time.sleep(30)  # Check every 30 seconds

        except Exception as e:
            print(f"❌ Error in trade monitoring: {e}")
            time.sleep(30)


def start_scheduler():
    print("📆 Scheduler started (Real PumpFun Trading)")

    # Start trade monitoring in background
    import threading
    monitor_thread = threading.Thread(target=monitor_trades, daemon=True)
    monitor_thread.start()

    while True:
        time.sleep(5)
