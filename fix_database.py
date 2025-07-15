#!/usr/bin/env python3
"""
Fix database issues by recreating the database properly
"""

import sqlite3
import os
import shutil

def fix_database():
    """Fix the database by recreating it properly"""
    print("🔧 Fixing database issues...")

    db_path = "db/trades.db"

    # Check if db directory exists
    if not os.path.exists("db"):
        print("📁 Creating db directory...")
        os.makedirs("db")

    # Backup existing database if it exists
    if os.path.exists(db_path):
        backup_path = "db/trades_backup.db"
        print(f"💾 Backing up existing database to {backup_path}")
        try:
            shutil.copy2(db_path, backup_path)
            print("✅ Backup created successfully")
        except Exception as e:
            print(f"⚠️  Could not create backup: {e}")

    # Remove corrupted database
    if os.path.exists(db_path):
        print("🗑️  Removing corrupted database...")
        try:
            os.remove(db_path)
            print("✅ Corrupted database removed")
        except Exception as e:
            print(f"❌ Could not remove database: {e}")

    # Create new database
    print("🆕 Creating new database...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create trades table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                mint_address TEXT NOT NULL,
                status TEXT NOT NULL,
                buy_price REAL,
                current_price REAL,
                pnl REAL,
                amount_sol REAL,
                time TEXT,
                transaction_signature TEXT
            )
        """)

        # Create some sample data for testing
        cursor.execute("""
            INSERT INTO trades (symbol, mint_address, status, buy_price, current_price, pnl, amount_sol, time, transaction_signature)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "TEST-TOKEN",
            "AXExPZNRHt54vhTPt6VvpcSoGNKMoMD4qGuMYEEzpump",
            "active",
            0.00001,
            0.00001,
            0.0,
            0.00001,
            "2025-01-12 20:00:00",
            "test_signature"
        ))

        conn.commit()
        conn.close()

        print("✅ Database created successfully")
        print("✅ Sample trade added for testing")

        # Test the database
        print("🧪 Testing database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM trades")
        count = cursor.fetchone()[0]
        conn.close()

        print(f"✅ Database test successful - {count} trades found")

    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

    print("\n📊 Database Status:")
    print("✅ Database file created: db/trades.db")
    print("✅ Trades table created with proper schema")
    print("✅ Sample data added for testing")
    print("✅ Dashboard should now work correctly")

    return True

if __name__ == "__main__":
    fix_database()