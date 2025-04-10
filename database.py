import sqlite3
import pandas as pd


def init_db():
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 trader TEXT,
                 commodity TEXT,
                 type TEXT,
                 quantity INTEGER,
                 price REAL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def insert_trade(trader, commodity, trade_type, quantity, price):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('INSERT INTO trades (trader, commodity, type, quantity, price) VALUES (?, ?, ?, ?, ?)',
              (trader, commodity, trade_type, quantity, price))
    conn.commit()
    conn.close()

def fetch_all_trades():
    conn = sqlite3.connect('trades.db')
    df = pd.read_sql_query('SELECT * FROM trades', conn)
    conn.close()
    return df
