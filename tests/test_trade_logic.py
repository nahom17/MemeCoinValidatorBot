import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trade_logic import TradeTracker

def test_take_profit():
    tracker = TradeTracker(entry_price=1.0)
    # Simulate price reaching 3x
    result = tracker.update_price(3.0)
    assert result == "take_profit"

def test_stop_loss():
    tracker = TradeTracker(entry_price=1.0)
    tracker.update_price(2.0)  # Peak at 2.0
    # Drop below trailing stop (20% below peak)
    result = tracker.update_price(1.5)
    assert result == "stop_loss"

def test_hold():
    tracker = TradeTracker(entry_price=1.0)
    result = tracker.update_price(1.1)
    assert result == "hold"