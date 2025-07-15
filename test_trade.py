#!/usr/bin/env python3
"""
Test trading functionality with the user's specific token
"""

import os
from dotenv import load_dotenv
from bot.trader import trade_local

def test_trade():
    """Test trading with the specific token"""
    print("🔍 Testing trade functionality...")

    # Load environment variables
    load_dotenv()
    private_key = os.getenv("PRIVATE_KEY")

    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return

    # Your token address
    token_address = "AXExPZNRHt54vhTPt6VvpcSoGNKMoMD4qGuMYEEzpump"

    print(f"🎯 Testing trade with token: {token_address}")
    print("⚠️  This will attempt a real trade with 0.01 SOL")
    print("⚠️  Make sure you want to proceed!")

    # Ask for confirmation
    response = input("Do you want to proceed with the test trade? (y/N): ")
    if response.lower() != 'y':
        print("❌ Test cancelled")
        return

    try:
        # Test buy trade
        print("\n🚀 Executing test buy trade...")
        signature = trade_local(
            private_key=private_key,
            token_mint=token_address,
            side="buy",
            amount_sol=0.01
        )

        print(f"✅ Test trade successful!")
        print(f"🔗 Transaction: https://solscan.io/tx/{signature}")

    except Exception as e:
        print(f"❌ Test trade failed: {e}")
        print("This might be due to:")
        print("1. Insufficient SOL balance")
        print("2. Token not available for trading")
        print("3. Network issues")
        print("4. API rate limiting")

if __name__ == "__main__":
    test_trade()