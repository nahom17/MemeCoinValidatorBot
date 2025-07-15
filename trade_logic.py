import random
from utils.log_print import log_print

class TradeTracker:
    def __init__(self, entry_price):
        self.entry_price = entry_price
        self.peak_price = entry_price
        self.trailing_stop_pct = 0.20  # 20% trailing stop
        self.take_profit_x = 3  # take profit if 3x

    def update_price(self, current_price):
        if current_price > self.peak_price:
            self.peak_price = current_price

        if current_price >= self.entry_price * self.take_profit_x:
            log_print(f"🎯 Profit target reached! {current_price:.4f} SOL (3x). Sell now!")
            return "take_profit"

        if current_price <= self.peak_price * (1 - self.trailing_stop_pct):
            log_print(f"🔻 Price dropped below trailing stop: {current_price:.4f} SOL. Sell to protect gains.")
            return "stop_loss"

        log_print(f"📊 Current: {current_price:.4f}, Entry: {self.entry_price:.4f}, Peak: {self.peak_price:.4f}")
        return "hold"