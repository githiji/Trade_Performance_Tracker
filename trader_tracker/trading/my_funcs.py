import datetime
from bs4 import BeautifulSoup


from bs4 import BeautifulSoup
import datetime

def readfile(content):
    soup = BeautifulSoup(content, 'html.parser')
    trades = []

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
