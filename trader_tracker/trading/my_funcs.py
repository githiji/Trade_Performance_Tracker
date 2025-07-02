import MetaTrader5 as mt5
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests


# Define global trade list
trades = []

# Format example: 2024.06.03 12:35:42
HTML_DATETIME_FORMAT = "%Y.%m.%d %H:%M:%S"

# Define date range for MT5

to_date = datetime.now()
from_date = to_date - timedelta(days=30)

# ✅ Function to read trade history from an MT5-exported HTML report
def readfile(content):
    soup = BeautifulSoup(content, 'html.parser')
    rows = soup.find_all('tr')[1:]  # Skip header row

    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 14:
            continue  # Skip incomplete rows

        try:
            trade = {
                "ticket": cells[0].text.strip(),
                "open_time": datetime.strptime(cells[1].text.strip(), HTML_DATETIME_FORMAT),
                "type": cells[2].text.strip().upper(),
                "lot_size": float(cells[3].text.strip()),
                "symbol": cells[4].text.strip(),
                "entry_price": float(cells[5].text.strip()),
                "stop_loss": float(cells[6].text.strip()),
                "take_profit": float(cells[7].text.strip()),
                "close_time": datetime.strptime(cells[8].text.strip(), HTML_DATETIME_FORMAT),
                "exit_price": float(cells[9].text.strip()),
                "profit": float(cells[13].text.strip()),  # Usually index 13 is "Profit"
            }
            trades.append(trade)
        except Exception as e:
            print(f"[HTML ERROR] {e}")
    return trades

# ✅ Function to collect MT5 trades from the terminal
def mt5_auto_collect():
    if not mt5.initialize():
        print("MT5 failed to initialize:", mt5.last_error())
        return []

    history = mt5.history_deals_get(from_date, to_date)
    
    if history is None:
        print("No trade history found")
        mt5.shutdown()
        return []

    collected = []

    for deal in history:
        trade_data = {
            "ticket": deal.ticket,
            "open_time": datetime.fromtimestamp(deal.time),
            "type": "BUY" if deal.type == 0 else "SELL",
            "lot_size": deal.volume,
            "symbol": deal.symbol,
            "entry_price": deal.price,
            "exit_price": deal.price,  # You may need to get this from a `history_orders_get`
            "profit_loss": deal.profit,
            "user": 1  # TODO: Replace with actual user ID or auth mechanism
        }
        collected.append(trade_data)

    mt5.shutdown()
    return collected
