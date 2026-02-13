import yfinance as yf
import json
import os
from datetime import datetime

def create_market_indices():
    print("Fetching market indices...")
    
    indices_map = {
        '^DJI': 'Dow Jones',
        '^GSPC': 'S&P 500',
        '^IXIC': 'NASDAQ',
        '^RUT': 'Russell 2000',
        '^VIX': 'VIX',
        'GC=F': 'Gold',
        'CL=F': 'Crude Oil',
        'BTC-USD': 'Bitcoin',
        '^TNX': '10Y Treasury',
        'DX-Y.NYB': 'Dollar Index',
        'KRW=X': 'USD/KRW'
    }
    
    market_indices = []
    
    for ticker, name in indices_map.items():
        try:
            print(f"  - Fetching {name} ({ticker})...")
            stock = yf.Ticker(ticker)
            # Fetch 5 days to ensure we get closed data
            hist = stock.history(period='5d')
            
            if not hist.empty and len(hist) >= 2:
                current_val = float(hist['Close'].iloc[-1])
                prev_val = float(hist['Close'].iloc[-2])
                change = current_val - prev_val
                change_pct = (change / prev_val) * 100
                
                market_indices.append({
                    'name': name,
                    'price': f"{current_val:,.2f}",
                    'change': f"{change:+,.2f}",
                    'change_pct': round(change_pct, 2),
                    'color': 'green' if change >= 0 else 'red'
                })
            elif not hist.empty:
                current_val = float(hist['Close'].iloc[-1])
                market_indices.append({
                    'name': name,
                    'price': f"{current_val:,.2f}",
                    'change': "0.00",
                    'change_pct': 0,
                    'color': 'gray'
                })
            else:
                 print(f"    No data for {ticker}")
                 
        except Exception as e:
            print(f"    Error fetching {ticker}: {e}")

    data = {
        'market_indices': market_indices,
        'top_holdings': [], # Placeholder
        'style_box': {},    # Placeholder
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('market_indices.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Saved {len(market_indices)} indices to market_indices.json")

if __name__ == "__main__":
    create_market_indices()
