# Yahoo Finance BigQuery Pipeline with Dash Dashboard# Google Cloud ETL Pipeline



A comprehensive real-time financial data pipeline that collects live market data from Yahoo Finance and Alpha Vantage APIs, stores it in Google BigQuery, and presents insights through an interactive web dashboard built with Plotly Dash.**Author:** Pedro Siqueira



## Project Overview## About This Project



This project demonstrates a complete data engineering workflow from data collection to visualization. The system fetches real-time stock prices and cryptocurrency data, processes and stores the information in Google Cloud infrastructure, and provides an interactive dashboard for monitoring market performance.I built this ETL pipeline to learn how to work with Google Cloud Platform and process real data in the cloud. 



## Architecture## What It Does



The pipeline consists of three main components:The pipeline takes sales data from CSV files and processes it through Google Cloud:



1. **Data Collection Layer**: Fetches live financial data from Yahoo Finance API for stocks and Alpha Vantage API for cryptocurrency prices```

2. **Storage Layer**: Uses Google Cloud Storage for raw data files and BigQuery for structured data warehouseCSV File → Python Processing → Cloud Storage → BigQuery → Analytics

3. **Visualization Layer**: Interactive Plotly Dash web application that queries BigQuery and displays real-time market data```



## Features**The process:**

1. **Extract** - Reads data from CSV files and validates it

### Data Pipeline2. **Transform** - Cleans the data and adds calculated fields using pandas

- Real-time stock price collection using Yahoo Finance API3. **Load** - Saves data to Google Cloud Storage and BigQuery

- Cryptocurrency data integration via Alpha Vantage API4. **Analyze** - Runs SQL queries to get business insights

- Automated data processing and cleaning

- Google Cloud Storage integration for data persistence## Tools I Used

- BigQuery data warehouse with optimized schemas

- Historical data tracking with timestamp-based records- **Python** - Main programming language for the pipeline

- **Pandas** - For cleaning and transforming the data

### Interactive Dashboard- **Google Cloud Storage** - To store the processed files

- Live price updates every 30 seconds- **BigQuery** - Google's data warehouse for running queries

- Market summary cards showing portfolio overview- **Google Cloud IAM** - For secure authentication

- Best and worst performer identification

- Trading volume analysis## What I Learned

- Interactive price trend charts

- Performance comparison visualizations**Working with Cloud Services:**

- Responsive design for desktop and mobile- How to set up and use Google Cloud Storage buckets

- Creating and managing BigQuery datasets and tables

### Market Analytics- Setting up proper authentication with service accounts

- Portfolio performance metrics- Handling errors when working with cloud APIs

- Gaining vs declining stocks analysis

- Average market performance calculations**Data Processing:**

- Real-time price change indicators- Reading and validating CSV data with pandas

- Trading volume summaries- Adding business logic to transform raw data

- Creating automated data quality checks

## Technology Stack- Building reusable code that handles different data sources



**Programming Language**: Python 3.11+**What you need:**

- Python 3.x with pandas installed

**APIs and Data Sources**:- A Google Cloud account

- Yahoo Finance (yfinance library)- Service account credentials (JSON file)

- Alpha Vantage API- BigQuery and Cloud Storage enabled in your project



**Cloud Infrastructure**:## Code Structure

- Google Cloud Platform

- Google Cloud StorageThe main file `pipeline_to_GC.py` contains:

- Google BigQuery- `CloudETLPipeline` class that handles all the processing

- Google Cloud IAM- Methods for extracting, transforming, and loading data

- Error handling for when things go wrong

**Data Processing**:- SQL queries for generating business reports

- Pandas for data manipulation

- Requests for API calls## Next Steps

- JSON for data serialization

Things I want to add in the future:

**Visualization**:- Schedule the pipeline to run automatically

- Plotly for interactive charts- Add more data sources like APIs or databases

- Dash for web application framework- Create better monitoring and alerts

- HTML/CSS for styling- Build a dashboard to visualize the results



## Installation and Setup## Connection



### PrerequisitesThis project builds on my previous work with Excel and APIs that you can see here: https://github.com/siqueiranetopedro/Pipelines_Excel-API

- Python 3.11 or higher

- Google Cloud Platform accountFeel free to look at the code and reach out if you have questions about how it works.

- Alpha Vantage API key (free tier available)

---

### Required Python Packages

```bash**Pedro Siqueira**  

pip install pandas requests google-cloud-storage google-cloud-bigquery yfinance plotly dash pandas-gbqLearning data engineering and cloud technologies

```

### Google Cloud Setup
1. Create a new Google Cloud Project
2. Enable BigQuery and Cloud Storage APIs
3. Create a service account with appropriate permissions
4. Download the service account key file
5. Set the GOOGLE_APPLICATION_CREDENTIALS environment variable

### API Configuration
1. Sign up for a free Alpha Vantage API key at https://www.alphavantage.co/support/#api-key
2. Update the API key in the pipeline configuration

## Usage

### Running the Data Pipeline
Execute the data collection pipeline to fetch fresh market data:
```bash
python realtime_financial_pipeline.py
```

This will:
- Fetch current stock prices for AAPL, GOOGL, MSFT, TSLA, AMZN
- Collect Bitcoin exchange rate data
- Store raw data in Google Cloud Storage
- Load processed data into BigQuery tables

### Starting the Dashboard
Launch the interactive web dashboard:
```bash
python financial_dashboard.py
```

Access the dashboard at http://localhost:8050

### Data Verification
Check the current data status and validate pipeline execution:
```bash
python verify_realtime_data.py
```

## File Structure

- `realtime_financial_pipeline.py` - Main data collection and processing pipeline
- `financial_dashboard.py` - Interactive Plotly Dash web application
- `verify_realtime_data.py` - Data validation and pipeline verification utility

## Data Schema

### Stock Prices Table (realtime_stock_prices)
- symbol: Stock ticker symbol
- price: Current stock price
- change: Price change from previous close
- change_percent: Percentage change
- volume: Trading volume
- timestamp: Data collection timestamp
- Additional OHLC data (open, high, low, close)

### Cryptocurrency Table (realtime_crypto_prices)
- from_currency: Source currency (BTC)
- to_currency: Target currency (USD)
- exchange_rate: Current exchange rate
- bid_price: Current bid price
- ask_price: Current ask price
- timestamp: Data collection timestamp

## Dashboard Features

### Market Summary Section
- Overall market status (gaining vs declining stocks)
- Average portfolio performance
- Best performing stock of the day
- Worst performing stock of the day
- Total trading volume across tracked stocks

### Individual Stock Cards
- Current price with color-coded change indicators
- Percentage change from previous close
- Trading volume information
- Up/down arrows for quick performance assessment

### Interactive Charts
- Price trend visualization over time
- Performance comparison bar charts
- Real-time data updates every 30 seconds

## Cost Considerations

This project is designed to operate within Google Cloud's free tier limits:
- BigQuery: 1TB queries per month (free)
- Cloud Storage: 5GB storage (free)
- Minimal data transfer costs

Typical monthly costs for moderate usage: $0.00 - $0.10

## Performance Optimization

- Efficient BigQuery schema design for fast queries
- Optimized API calls with appropriate rate limiting
- Cached data processing to minimize computation overhead
- Responsive dashboard design for quick load times

## Future Enhancements

Potential areas for expansion:
- Additional stock symbols and market indices
- Technical indicators and moving averages
- Price alert notifications
- Portfolio tracking with investment amounts
- Historical backtesting capabilities
- Mobile application development
- Automated deployment with CI/CD pipelines

## Contributing

This project serves as a demonstration of modern data engineering practices. Feel free to fork and extend the functionality for your own use cases.

## License

This project is available under the MIT License. See LICENSE file for details.

## Author

Pedro Siqueira  
Data Engineer & Analytics Professional

## Acknowledgments

- Yahoo Finance for providing reliable financial data API
- Alpha Vantage for cryptocurrency market data
- Google Cloud Platform for scalable infrastructure
- Plotly team for excellent visualization tools