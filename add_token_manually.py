#!/usr/bin/env python3
"""
Manually add tokens to the bot for trading
"""

import json
import os

def add_token_manually():
    """Add a token manually to the bot"""
    print("🎯 Manual Token Addition")
    print("=" * 50)

    print("Since PumpFun loads tokens dynamically, you can manually add tokens here.")
    print("This will allow the bot to trade these tokens when detected.")

    # Get token details from user
    print("\n📝 Enter token details:")

    token_address = input("Token address (mint): ").strip()
    if not token_address:
        print("❌ Token address is required")
        return

    symbol = input("Token symbol (optional): ").strip() or "Unknown"
    creator = input("Creator (optional): ").strip() or "unknown"

    # Create token info
    token_info = {
        "symbol": symbol,
        "mint": token_address,
        "address": token_address,
        "creator": creator,
        "sol_raised": 0
    }

    print(f"\n✅ Token added:")
    print(f"   Symbol: {symbol}")
    print(f"   Address: {token_address}")
    print(f"   Creator: {creator}")

    # Save to a file for the bot to read
    tokens_file = "manual_tokens.json"

    # Load existing tokens
    existing_tokens = []
    if os.path.exists(tokens_file):
        try:
            with open(tokens_file, 'r') as f:
                existing_tokens = json.load(f)
        except:
            existing_tokens = []

    # Add new token if not already present
    token_exists = any(t.get('mint') == token_address for t in existing_tokens)
    if not token_exists:
        existing_tokens.append(token_info)

        # Save updated list
        with open(tokens_file, 'w') as f:
            json.dump(existing_tokens, f, indent=2)

        print(f"✅ Token saved to {tokens_file}")
        print(f"📊 Total manual tokens: {len(existing_tokens)}")
    else:
        print("⚠️  Token already exists in manual list")

    print("\n💡 The bot will now monitor this token for trading opportunities")
    print("💡 You can add more tokens by running this script again")

def list_manual_tokens():
    """List all manually added tokens"""
    tokens_file = "manual_tokens.json"

    if os.path.exists(tokens_file):
        try:
            with open(tokens_file, 'r') as f:
                tokens = json.load(f)

            print(f"📋 Manual Tokens ({len(tokens)}):")
            for i, token in enumerate(tokens, 1):
                print(f"   {i}. {token['symbol']} - {token['mint']}")
        except Exception as e:
            print(f"❌ Error reading tokens: {e}")
    else:
        print("📋 No manual tokens found")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Add new token")
    print("2. List existing tokens")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        add_token_manually()
    elif choice == "2":
        list_manual_tokens()
    else:
        print("❌ Invalid choice")