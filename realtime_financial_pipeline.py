#!/usr/bin/env python3
"""
Enhanced Financial Data API Pipeline with REAL-TIME data
Using Yahoo Finance for live stock data + Alpha Vantage for crypto
Author: Pedro Siqueira
Flow: Yahoo Finance API + Alpha Vantage → Google Cloud Storage → BigQuery → Dashboard
"""

import pandas as pd
import requests
import json
import yfinance as yf
from datetime import datetime, timedelta
import time
from google.cloud import storage, bigquery
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedFinancialDataPipeline:
    def __init__(self):
        """Initialize the enhanced financial data pipeline"""
        # Set up Google Cloud credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/pedrosiqueira/Desktop/pedro-credentials.json'
        
        # Alpha Vantage API for crypto (still good for this)
        self.alpha_vantage_key = "CP0LPHT991QU0TPY"
        self.alpha_vantage_url = "https://www.alphavantage.co/query"
        
        # Google Cloud Configuration
        self.project_id = "symbolic-axe-474621-e8"
        self.dataset_id = "financial_data"
        self.bucket_name = "financial-data-symbolic-axe"
        
        # Initialize clients
        self.storage_client = storage.Client()
        self.bq_client = bigquery.Client()
        
        # Stock symbols to track
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
        
    def fetch_realtime_stock_data(self):
        """Fetch REAL-TIME stock data using Yahoo Finance"""
        try:
            logger.info("Fetching real-time stock data from Yahoo Finance")
            
            # Download real-time data for all symbols
            data = yf.download(self.symbols, period="1d", interval="1m", progress=False)
            
            if data.empty:
                logger.error("No data received from Yahoo Finance")
                return []
            
            # Get the latest data point for each symbol
            latest_data = data.iloc[-1]
            latest_time = data.index[-1]
            
            stock_records = []
            
            for symbol in self.symbols:
                try:
                    # Get detailed info for each stock
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    # Extract data from the latest minute
                    current_price = latest_data[('Close', symbol)]
                    volume = latest_data[('Volume', symbol)]
                    open_price = latest_data[('Open', symbol)]
                    high_price = latest_data[('High', symbol)]
                    low_price = latest_data[('Low', symbol)]
                    
                    # Get additional info from ticker info
                    previous_close = info.get('regularMarketPreviousClose', current_price)
                    
                    # Calculate change
                    change = current_price - previous_close
                    change_percent = (change / previous_close * 100) if previous_close != 0 else 0
                    
                    stock_record = {
                        'symbol': symbol,
                        'price': float(current_price),
                        'change': float(change),
                        'change_percent': f"{change_percent:.4f}",
                        'volume': int(volume) if pd.notna(volume) else 0,
                        'latest_trading_day': latest_time.strftime('%Y-%m-%d'),
                        'previous_close': float(previous_close),
                        'open': float(open_price),
                        'high': float(high_price),
                        'low': float(low_price),
                        'timestamp': datetime.now().isoformat(),
                        'data_source': 'yahoo_finance'
                    }
                    
                    stock_records.append(stock_record)
                    logger.info(f"✅ {symbol}: ${current_price:.2f} ({change_percent:+.2f}%) - LIVE DATA")
                    
                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")
                    continue
            
            return stock_records
            
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data: {e}")
            return []
    
    def fetch_crypto_data(self):
        """Fetch crypto data from Alpha Vantage (still good for crypto)"""
        try:
            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': 'BTC',
                'to_currency': 'USD',
                'apikey': self.alpha_vantage_key
            }
            
            logger.info("Fetching Bitcoin data from Alpha Vantage")
            response = requests.get(self.alpha_vantage_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if "Realtime Currency Exchange Rate" in data:
                    rate_data = data["Realtime Currency Exchange Rate"]
                    
                    crypto_record = {
                        'from_currency': rate_data["1. From_Currency Code"],
                        'to_currency': rate_data["3. To_Currency Code"],
                        'exchange_rate': float(rate_data["5. Exchange Rate"]),
                        'last_refreshed': rate_data["6. Last Refreshed"],
                        'timezone': rate_data["7. Time Zone"],
                        'bid_price': float(rate_data["8. Bid Price"]),
                        'ask_price': float(rate_data["9. Ask Price"]),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    bitcoin_price = crypto_record['exchange_rate']
                    logger.info(f"✅ Bitcoin: ${bitcoin_price:,.2f}")
                    
                    return [crypto_record]
                else:
                    logger.error(f"Invalid crypto response: {data}")
                    return []
            else:
                logger.error(f"Crypto API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching crypto data: {e}")
            return []
    
    def upload_to_gcs(self, data, file_prefix):
        """Upload data to Google Cloud Storage"""
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"financial_data/{file_prefix}/{timestamp}_{file_prefix}.json"
            
            blob = bucket.blob(filename)
            blob.upload_from_string(json.dumps(data, indent=2))
            
            logger.info(f"Uploaded {file_prefix} data to GCS: {filename}")
            
        except Exception as e:
            logger.error(f"Error uploading to GCS: {e}")
    
    def load_to_bigquery(self, df, table_name):
        """Load DataFrame to BigQuery"""
        try:
            # Create dataset if it doesn't exist
            dataset_ref = self.bq_client.dataset(self.dataset_id)
            try:
                self.bq_client.get_dataset(dataset_ref)
            except:
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = "US"
                self.bq_client.create_dataset(dataset)
                logger.info(f"Created dataset {self.dataset_id}")
            
            # Define table reference
            table_ref = dataset_ref.table(table_name)
            
            # Configure load job
            job_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_APPEND",  # Append new data for time series
                autodetect=True
            )
            
            # Load data
            job = self.bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()
            
            logger.info(f"✅ Loaded {len(df)} rows to BigQuery table {table_name}")
            
        except Exception as e:
            logger.error(f"Error loading to BigQuery: {e}")
    
    def run_enhanced_pipeline(self):
        """Run the enhanced real-time financial data pipeline"""
        logger.info("🚀 Starting Enhanced Real-Time Financial Data Pipeline")
        
        # Fetch real-time stock data from Yahoo Finance
        stock_data = self.fetch_realtime_stock_data()
        
        if stock_data:
            # Upload to GCS
            self.upload_to_gcs(stock_data, "stocks")
            
            # Load to BigQuery
            stock_df = pd.DataFrame(stock_data)
            self.load_to_bigquery(stock_df, "realtime_stock_prices")
        
        # Wait to respect API limits
        time.sleep(5)
        
        # Fetch crypto data from Alpha Vantage
        crypto_data = self.fetch_crypto_data()
        
        if crypto_data:
            # Upload to GCS
            self.upload_to_gcs(crypto_data, "crypto")
            
            # Load to BigQuery
            crypto_df = pd.DataFrame(crypto_data)
            self.load_to_bigquery(crypto_df, "realtime_crypto_prices")
        
        logger.info("🎉 Enhanced Pipeline execution completed successfully!")

def main():
    """Main function to run the enhanced pipeline"""
    pipeline = EnhancedFinancialDataPipeline()
    pipeline.run_enhanced_pipeline()

if __name__ == "__main__":
    main()