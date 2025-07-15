#!/usr/bin/env python3
"""
Test trading functionality with a tiny amount to check minimal liquidity
"""

import os
from dotenv import load_dotenv
from bot.trader import trade_local

def test_tiny_trade():
    """Test trading with a tiny amount"""
    print("🔍 Testing trade functionality with tiny amount...")

    # Load environment variables
    load_dotenv()
    private_key = os.getenv("PRIVATE_KEY")

    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return

    # Your token address
    token_address = "AXExPZNRHt54vhTPt6VvpcSoGNKMoMD4qGuMYEEzpump"

    print(f"🎯 Testing trade with token: {token_address}")
    print("⚠️  This will attempt a real trade with 0.0001 SOL (very small)")
    print("⚠️  Make sure you want to proceed!")

    # Ask for confirmation
    response = input("Do you want to proceed with the test trade? (y/N): ")
    if response.lower() != 'y':
        print("❌ Test cancelled")
        return

    try:
        # Test buy trade with tiny amount
        print("\n🚀 Executing test buy trade with 0.0001 SOL...")
        signature = trade_local(
            private_key=private_key,
            token_mint=token_address,
            side="buy",
            amount_sol=0.0001  # Extremely small amount
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
        print("5. Token has extremely low liquidity")
        print("6. Minimum trade amount not met")

if __name__ == "__main__":
    test_tiny_trade()