import pandas as pd
import os
from datetime import datetime, timedelta

def create_light_csv():
    input_file = 'us_daily_prices.csv'
    output_file = 'us_daily_prices_light.csv'
    
    print(f"Reading {input_file}...")
    try:
        # Read only necessary columns if possible, but reading all for now
        df = pd.read_csv(input_file)
        
        # Convert Date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Filter for last 1 year
        one_year_ago = datetime.now() - timedelta(days=365)
        df_light = df[df['date'] >= one_year_ago]
        
        print(f"Original rows: {len(df)}")
        print(f"Light rows: {len(df_light)}")
        
        # Save to new file
        df_light.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
        
        # Check size
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"File size: {size_mb:.2f} MB")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_light_csv()
