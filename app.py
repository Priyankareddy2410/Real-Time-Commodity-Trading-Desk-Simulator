import streamlit as st
import pandas as pd
from trade_engine import calculate_unrealized_pnl, get_current_price
from database import init_db, insert_trade, fetch_all_trades

# Initialize DB
init_db()

# Load simulated market prices
price_df = pd.read_csv("data/market_prices.csv")

st.title("📊 Real-Time Commodity Trading Desk Simulator")

# Trade input form
with st.form("trade_form"):
    trader = st.text_input("Your Name", "Priya")
    commodity = st.selectbox("Commodity", price_df["Commodity"].tolist())
    trade_type = st.selectbox("Trade Type", ["Buy", "Sell"])
    quantity = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Trade Price", format="%.2f")
    submit = st.form_submit_button("Submit Trade")

if submit:
    insert_trade(trader, commodity, trade_type, quantity, price)
    st.success(f"{trade_type} {quantity} units of {commodity} at ${price} submitted!")

# Show all trades
st.subheader("📜 Trade History")
trades_df = fetch_all_trades()
st.dataframe(trades_df)

# Calculate and display P&L
if not trades_df.empty:
    st.subheader("📈 P&L Summary")
    pnl_data = []

    for _, row in trades_df.iterrows():
        current_price = get_current_price(row["commodity"], price_df)
        unrealized = calculate_unrealized_pnl(
            trade_price=row["price"],
            current_price=current_price,
            quantity=row["quantity"],
            trade_type=row["type"]
        )
        pnl_data.append({
            "Commodity": row["commodity"],
            "Trade Type": row["type"],
            "Quantity": row["quantity"],
            "Entry Price": row["price"],
            "Current Price": current_price,
            "Unrealized P&L": round(unrealized, 2)
        })

    pnl_df = pd.DataFrame(pnl_data)
    st.dataframe(pnl_df)
    st.metric("📊 Total Unrealized P&L", f"${pnl_df['Unrealized P&L'].sum():,.2f}")
