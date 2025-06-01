import datetime
from bs4 import BeautifulSoup

def readfile(html_file):
    soup = BeautifulSoup(html_file, 'html.parser')
    rows = soup.find_all('tr')[1:]  # Skip header row
    trades = []

    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 13:
            continue  # Skip incomplete rows

        try:
            # Read and parse each value safely
            trade = {
                "ticket": cells[0].text.strip(),
                "open_time": datetime.datetime.strptime(cells[1].text.strip(), "%Y.%m.%d %H:%M:%S"),
                "type": cells[2].text.strip().upper(),
                "lot_size": float(cells[3].text.strip().replace(',', '')),
                "symbol": cells[4].text.strip(),
                "entry_price": float(cells[5].text.strip().replace(',', '')),
                "s/l": float(cells[6].text.strip().replace(',', '')),
                "t/p": float(cells[7].text.strip().replace(',', '')),
                "close_time": datetime.datetime.strptime(cells[8].text.strip(), "%Y.%m.%d %H:%M:%S"),
                "exit_price": float(cells[9].text.strip().replace(',', '')),
                "profit": float(cells[12].text.strip().replace(',', ''))
            }
            trades.append(trade)

        except Exception as e:
            print(f"Error parsing row: {e}")  # Optional: log for debugging
            continue

    return trades
