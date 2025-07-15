#!/usr/bin/env python3
"""
Test trading with the newly added TRQMX token
"""

import os
from dotenv import load_dotenv
from bot.trader import trade_local

def test_new_token():
    """Test trading with the newly added TRQMX token"""
    print("🔍 Testing new token TRQMX...")

    # Load environment variables
    load_dotenv()
    private_key = os.getenv("PRIVATE_KEY")

    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return

    # New token address
    token_address = "AzCfxe9rMJhJr6vndQihnGAuzbxXibJ9SevzEU1apump"

    print(f"🎯 Testing trade with token: {token_address}")
    print("⚠️  This will attempt a real trade with 0.00001 SOL (minimal)")
    print("⚠️  Make sure you want to proceed!")

    # Ask for confirmation
    response = input("Do you want to proceed with the test trade? (y/N): ")
    if response.lower() != 'y':
        print("❌ Test cancelled")
        return

    try:
        # Test buy trade with minimal amount
        print("\n🚀 Executing test buy trade with 0.00001 SOL...")
        signature = trade_local(
            private_key=private_key,
            token_mint=token_address,
            side="buy",
            amount_sol=0.00001  # Minimal amount
        )

        print(f"✅ Test trade successful!")
        print(f"🔗 Transaction: https://solscan.io/tx/{signature}")

    except Exception as e:
        print(f"❌ Test trade failed: {e}")
        print("This confirms the token has low liquidity.")
        print("The bot will continue monitoring for tokens with better liquidity.")

if __name__ == "__main__":
    test_new_token()