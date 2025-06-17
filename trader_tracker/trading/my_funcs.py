import datetime
from bs4 import BeautifulSoup
import requests
import MetaTrader5 as mt5
import json
from datetime import datetime

from bs4 import BeautifulSoup
import datetime


from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
to_date = datetime.now()
trades = []

def readfile(content):
    soup = BeautifulSoup(content, 'html.parser')
   

    # Skip the header row by selecting rows after it
    rows = soup.find_all('tr')[1:]

    for row in rows:
        cells = row.find_all('td')
        
        # Skip empty or malformed rows
        if len(cells) < 13:
            continue
        
        try:
            trade = {
                "ticket": cells[0].text.strip(),
                "open_time": datetime.datetime.strptime(cells[1].text.strip(), "%Y.%m.%d %H:%M:%S"),
                "type": cells[2].text.strip().upper(),
                "lot_size": float(cells[3].text.strip()),
                "symbol": cells[4].text.strip(),
                "entry_price": float(cells[5].text.strip()),
                "stop_loss": float(cells[6].text.strip()),
                "take_profit": float(cells[7].text.strip()),
                "close_time": datetime.datetime.strptime(cells[8].text.strip(), "%Y.%m.%d %H:%M:%S"),
                "exit_price": float(cells[9].text.strip()),
                "profit": float(cells[13].text.strip()),
            }
            trades.append(trade)
        except Exception as e:
            print(f"Error parsing row: {e}")

    return trades


def mt5_auto_collect():
    history =  mt5.history_deals_get(from_date, to_date)
    if history is None:
        print("No trade history found")
        mt5.shutdown()
        quit()
    for deal in history:
        trade_data = {
            "ticket": deal.ticket,
            "open_time": datetime.fromtimestamp(deal.time),
            "type": "BUY" if deal.type == 0 else "SELL",
            "lot_size": deal.volume,
            "symbol": deal.symbol,
            "entry_price": deal.price,
            "exit_price": deal.price,  # Modify based on your logic
            "profit_loss": deal.profit,
            "user": 1  # Replace with the actual user ID or use token authentication
        }
        trades.append(trade_data)
        return trades