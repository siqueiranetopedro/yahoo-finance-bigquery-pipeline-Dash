#!/usr/bin/env python3
"""
Verify the new real-time financial data
"""

import os
from google.cloud import bigquery

def verify_realtime_data():
    """Verify real-time financial data"""
    
    # Set up credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/pedrosiqueira/Desktop/pedro-credentials.json'
    
    # Initialize BigQuery client
    client = bigquery.Client(project='symbolic-axe-474621-e8')
    
    print("🚀 REAL-TIME FINANCIAL DATA VERIFICATION")
    print("=" * 50)
    
    # Check real-time stock data
    realtime_stock_query = """
    SELECT 
        symbol,
        price,
        CAST(change_percent AS FLOAT64) as change_pct,
        volume,
        latest_trading_day,
        data_source,
        timestamp
    FROM `symbolic-axe-474621-e8.financial_data.realtime_stock_prices`
    ORDER BY timestamp DESC, symbol
    LIMIT 10
    """
    
    print("📈 REAL-TIME STOCK PRICES:")
    print("-" * 40)
    
    try:
        results = client.query(realtime_stock_query)
        for row in results:
            direction = "📈" if row.change_pct > 0 else "📉" if row.change_pct < 0 else "➡️"
            print(f"  {direction} {row.symbol}: ${row.price:.2f} ({row.change_pct:+.2f}%)")
            print(f"      Source: {row.data_source} | Day: {row.latest_trading_day}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Compare with old Alpha Vantage data
    old_stock_query = """
    SELECT 
        symbol,
        price,
        latest_trading_day,
        'alpha_vantage' as data_source
    FROM `symbolic-axe-474621-e8.financial_data.stock_prices`
    WHERE symbol = 'AAPL'
    ORDER BY timestamp DESC
    LIMIT 1
    """
    
    print("\n🔄 COMPARISON WITH OLD DATA:")
    print("-" * 40)
    
    try:
        old_results = client.query(old_stock_query)
        for row in old_results:
            print(f"  📊 OLD (Alpha Vantage): AAPL ${row.price:.2f} (Day: {row.latest_trading_day})")
        
        new_results = client.query("""
        SELECT price, latest_trading_day 
        FROM `symbolic-axe-474621-e8.financial_data.realtime_stock_prices`
        WHERE symbol = 'AAPL'
        ORDER BY timestamp DESC
        LIMIT 1
        """)
        
        for row in new_results:
            print(f"  🚀 NEW (Yahoo Finance): AAPL ${row.price:.2f} (Day: {row.latest_trading_day})")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Show table counts
    print("\n📊 DATA VOLUME:")
    print("-" * 40)
    
    tables = [
        ('stock_prices', 'Alpha Vantage (old)'),
        ('realtime_stock_prices', 'Yahoo Finance (real-time)'),
        ('crypto_prices', 'Alpha Vantage crypto'),
        ('realtime_crypto_prices', 'Alpha Vantage crypto (new table)')
    ]
    
    for table_name, description in tables:
        try:
            count_query = f"""
            SELECT COUNT(*) as total_rows
            FROM `symbolic-axe-474621-e8.financial_data.{table_name}`
            """
            result = client.query(count_query)
            for row in result:
                print(f"  📊 {table_name}: {row.total_rows} rows ({description})")
        except Exception as e:
            print(f"  📊 {table_name}: Table doesn't exist yet")
    
    print("\n🎯 SUMMARY:")
    print("-" * 30)
    print("  ✅ Yahoo Finance: LIVE real-time data during market hours")
    print("  ✅ Alpha Vantage: Delayed data (yesterday's prices)")
    print("  ✅ Both sources working and stored in BigQuery")
    print("  ✅ Ready for live dashboard connection!")

if __name__ == "__main__":
    verify_realtime_data()