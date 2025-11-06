# Yahoo Finance BigQuery Pipeline with Dash Dashboard

A real-time financial data pipeline that collects live market data from Yahoo Finance and Alpha Vantage APIs, stores it in Google BigQuery, and presents insights through an interactive web dashboard built with Plotly Dash.

<img width="3688" height="1986" alt="image" src="https://github.com/user-attachments/assets/4ba2dccf-a15f-42bd-8692-d5308d8b2a17" />

<img width="3678" height="1624" alt="image" src="https://github.com/user-attachments/assets/ed5571a0-9475-4eed-be6c-80970b8134a0" />
<img width="3674" height="1970" alt="image" src="https://github.com/user-attachments/assets/8f4470a2-9f78-4e1e-8f0e-d626eba8c9f4" />

## Project Overview

This project demonstrates a complete data engineering workflow from data collection to visualization. The system gets real-time stock prices and cryptocurrency data, processes and stores the information in Google Cloud database, and provides an interactive dashboard for monitoring market performance.

## What It Does

The pipeline is built to collect, process, and visualize real-time market data using cloud technologies. It connects live financial APIs to Google Cloud for storage and analytics, then sends the results to an interactive dashboard for visualization.

## Data Collection Layer

- Fetches live market data from Yahoo Finance API for stocks
- Retrieves cryptocurrency prices from Alpha Vantage API
- Cleans and formats the data using Python and pandas

## Storage Layer

- Stores raw files in Google Cloud Storage
- Loads processed tables into BigQuery for analytics
- Data flow: API → Python Processing → Cloud Storage → BigQuery → Analytics

## Visualization Layer

- Interactive Plotly Dash dashboard that queries BigQuery
- Displays live stock and crypto data with updates every 30 seconds
- Includes portfolio summaries, price trends, and performance comparisons

## The Process

1. **Extract**
   - Collects real-time stock prices from Yahoo Finance API
   - Pulls cryptocurrency data from Alpha Vantage API

2. **Transform**
   - Cleans and formats the data using pandas
   - Adds calculated fields like daily change and percent difference
   - Runs automatic checks to make sure the data is valid

3. **Load**
   - Saves processed data to Google Cloud Storage
   - Loads cleaned tables into BigQuery for analysis

4. **Analyze**
   - Runs SQL queries in BigQuery to get business insights
   - Tracks portfolio performance, market trends, and trading volumes

## Dashboard Features

- Live stock and crypto price updates every 30 seconds
- Portfolio overview with top gainers and decliners
- Real-time price trend and comparison charts
- Trading volume and market performance summaries
- Responsive layout for desktop and mobile

## Tools and Libraries

- Python 3.11+ as the main programming language
- pandas for cleaning and transforming data
- requests for API calls
- Plotly and Dash for interactive charts and dashboard
- Google Cloud Storage to store processed files
- BigQuery for analytics and SQL queries
- Google Cloud IAM for secure authentication with service accounts

## Market Analytics

- Set up secure authentication with Google service accounts
- Build portfolio performance metrics with error handling for API calls
- Compare gaining and declining stocks to identify trends
- Calculate average and cumulative market performance

## Data Processing

- Track real-time price changes and volume indicators
- Summarize trading activity by ticker and sector
- Apply logic to transform raw API data into structured insights
- Automate data validation and quality checks

## Working with Cloud Services

- Set up and manage Google Cloud Storage buckets
- Create and organize BigQuery datasets and tables
- Configure permissions using IAM service accounts

## Code Structure

**Main file: realtime_financial_pipeline.py**
- Contains the EnhancedFinancialDataPipeline class that handles:
- Extract, transform, and load steps
- Error handling for failed API calls
- SQL queries for analytics and reporting

**Dashboard files:**
- financial_dashboard.py – interactive Plotly Dash app
- verify_realtime_data.py – utility for checking data accuracy

## Setup and Requirements

### Prerequisites
- Python 3.11 or higher
- Google Cloud account with BigQuery and Storage enabled
- Alpha Vantage API key (free tier)
- Service account credentials (JSON file)

### Install Dependencies
```bash
pip install pandas requests google-cloud-storage google-cloud-bigquery yfinance plotly dash pandas-gbq
```

## How to Run

### Run the Data Pipeline
```bash
python realtime_financial_pipeline.py
```

This will:
- Fetch stock prices for AAPL, GOOGL, MSFT, TSLA, and AMZN
- Collect Bitcoin exchange rates
- Store raw files in Cloud Storage
- Load processed data into BigQuery

### Run the Dashboard
```bash
python financial_dashboard.py
```

Access the app at: http://localhost:8050

## Future Improvements

- Automate daily runs with Cloud Scheduler or CRON jobs
- Add new APIs and data sources
- Set up performance alerts and monitoring
- Add portfolio tracking and backtesting features

## What I Learned

- Building cloud-based ETL pipelines
- Working with Google Cloud (BigQuery, IAM, Storage)
- Managing real-time API data in Python
- Designing interactive dashboards for analytics

**Author: Pedro Siqueira**  
Learning Data Engineering and Cloud Technologies