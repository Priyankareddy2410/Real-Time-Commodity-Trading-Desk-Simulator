import pandas as pd

def calculate_unrealized_pnl(trade_price, current_price, quantity, trade_type):
    if trade_type == "Buy":
        return (current_price - trade_price) * quantity
    elif trade_type == "Sell":
        return (trade_price - current_price) * quantity
    return 0

def get_current_price(commodity, price_df):
    row = price_df[price_df['Commodity'] == commodity]
    if not row.empty:
        return float(row['Current_Price'].values[0])
    return None
