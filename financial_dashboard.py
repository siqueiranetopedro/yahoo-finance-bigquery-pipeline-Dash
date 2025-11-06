#!/usr/bin/env python3
"""
Interactive Financial Dashboard
Real-time stock price visualization using Plotly Dash
Author: Pedro Siqueira
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import pandas_gbq
from datetime import datetime, timedelta
import os
from google.cloud import bigquery
import time

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/pedrosiqueira/Desktop/pedro-credentials.json'

class FinancialDashboard:
    def __init__(self):
        """Initialize the financial dashboard"""
        self.project_id = "symbolic-axe-474621-e8"
        self.client = bigquery.Client(project=self.project_id)
        
        # Initialize Dash app
        self.app = dash.Dash(__name__)
        self.app.title = "Live Financial Dashboard"
        
        # Define layout
        self.setup_layout()
        self.setup_callbacks()
    
    def fetch_stock_data(self):
        """Fetch stock data from BigQuery"""
        query = """
        SELECT 
            symbol,
            price,
            CAST(change_percent AS FLOAT64) as change_percent,
            volume,
            latest_trading_day,
            timestamp,
            high,
            low,
            open
        FROM `symbolic-axe-474621-e8.financial_data.realtime_stock_prices`
        ORDER BY timestamp DESC
        """
        
        try:
            df = pandas_gbq.read_gbq(query, project_id=self.project_id)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()
    
    def fetch_crypto_data(self):
        """Fetch crypto data from BigQuery"""
        query = """
        SELECT 
            from_currency,
            exchange_rate,
            bid_price,
            ask_price,
            last_refreshed,
            timestamp
        FROM `symbolic-axe-474621-e8.financial_data.realtime_crypto_prices`
        ORDER BY timestamp DESC
        """
        
        try:
            df = pandas_gbq.read_gbq(query, project_id=self.project_id)
            return df
        except Exception as e:
            print(f"Error fetching crypto data: {e}")
            return pd.DataFrame()
    
    def get_latest_prices(self):
        """Get latest price for each symbol"""
        df = self.fetch_stock_data()
        if df.empty:
            return pd.DataFrame()
        
        # Get latest price for each symbol
        latest_df = df.loc[df.groupby('symbol')['timestamp'].idxmax()]
        return latest_df
    
    def get_price_history(self):
        """Get price history for trend analysis"""
        df = self.fetch_stock_data()
        if df.empty:
            return pd.DataFrame()
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.sort_values('timestamp')
    
    def setup_layout(self):
        """Set up the dashboard layout"""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("Live Financial Dashboard", 
                       style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': '30px'}),
                html.P(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                       style={'textAlign': 'center', 'color': '#666', 'fontSize': '14px'})
            ], style={'padding': '20px'}),
            
            # Auto-refresh interval
            dcc.Interval(
                id='interval-component',
                interval=30*1000,  # Update every 30 seconds
                n_intervals=0
            ),
            
            # Market Summary Section
            html.Div([
                html.H2("Market Summary", style={'color': '#2E86AB'}),
                html.Div(id="market-summary", children=[])
            ], style={'padding': '20px'}),
            
            # Current Prices Section
            html.Div([
                html.H2("Current Stock Prices", style={'color': '#2E86AB'}),
                html.Div(id="current-prices", children=[])
            ], style={'padding': '20px'}),
            
            # Price Trends Chart
            html.Div([
                html.H2("Price Trends", style={'color': '#2E86AB'}),
                dcc.Graph(id="price-trends-chart")
            ], style={'padding': '20px'}),
            
            # Performance Chart
            html.Div([
                html.H2("Performance Comparison", style={'color': '#2E86AB'}),
                dcc.Graph(id="performance-chart")
            ], style={'padding': '20px'}),
            
            # Crypto Section
            html.Div([
                html.H2("Cryptocurrency", style={'color': '#2E86AB'}),
                html.Div(id="crypto-prices", children=[])
            ], style={'padding': '20px'})
        ])
    
    def setup_callbacks(self):
        """Set up dashboard callbacks for interactivity"""
        
        @self.app.callback(
            [Output('market-summary', 'children'),
             Output('current-prices', 'children'),
             Output('price-trends-chart', 'figure'),
             Output('performance-chart', 'figure'),
             Output('crypto-prices', 'children')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_dashboard(n):
            """Update all dashboard components"""
            
            # Get latest prices
            latest_df = self.get_latest_prices()
            price_history = self.get_price_history()
            crypto_df = self.fetch_crypto_data()
            
            # Create market summary cards
            market_summary_cards = []
            if not latest_df.empty:
                # Calculate market statistics
                total_stocks = len(latest_df)
                gaining_stocks = len(latest_df[latest_df['change_percent'] > 0])
                losing_stocks = len(latest_df[latest_df['change_percent'] < 0])
                flat_stocks = total_stocks - gaining_stocks - losing_stocks
                avg_performance = latest_df['change_percent'].mean()
                total_volume = latest_df['volume'].sum()
                
                # Best and worst performers
                best_performer = latest_df.loc[latest_df['change_percent'].idxmax()]
                worst_performer = latest_df.loc[latest_df['change_percent'].idxmin()]
                
                summary_cards = [
                    # Market Overview Card
                    html.Div([
                        html.H4("Market Overview", style={'margin': '0 0 10px 0', 'color': '#333'}),
                        html.P(f"↑ {gaining_stocks} Gaining", style={'margin': '2px 0', 'color': '#28a745', 'fontWeight': 'bold'}),
                        html.P(f"↓ {losing_stocks} Declining", style={'margin': '2px 0', 'color': '#dc3545', 'fontWeight': 'bold'}),
                        html.P(f"→ {flat_stocks} Flat", style={'margin': '2px 0', 'color': '#6c757d'}),
                        html.P(f"Avg: {avg_performance:+.2f}%", style={'margin': '5px 0 0 0', 'fontSize': '14px', 'fontWeight': 'bold'})
                    ], style={
                        'border': '1px solid #ddd',
                        'borderRadius': '8px',
                        'padding': '15px',
                        'margin': '10px',
                        'backgroundColor': '#f8f9fa',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'width': '200px',
                        'display': 'inline-block',
                        'verticalAlign': 'top'
                    }),
                    
                    # Best Performer Card
                    html.Div([
                        html.H4("Best Performer", style={'margin': '0 0 10px 0', 'color': '#333'}),
                        html.H3(f"↑ {best_performer['symbol']}", style={'margin': '0', 'color': '#28a745'}),
                        html.P(f"${best_performer['price']:.2f}", style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold'}),
                        html.P(f"+{best_performer['change_percent']:.2f}%", style={'margin': '0', 'color': '#28a745', 'fontWeight': 'bold'})
                    ], style={
                        'border': '1px solid #28a745',
                        'borderRadius': '8px',
                        'padding': '15px',
                        'margin': '10px',
                        'backgroundColor': '#d4edda',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'width': '180px',
                        'display': 'inline-block',
                        'verticalAlign': 'top'
                    }),
                    
                    # Worst Performer Card
                    html.Div([
                        html.H4("Worst Performer", style={'margin': '0 0 10px 0', 'color': '#333'}),
                        html.H3(f"↓ {worst_performer['symbol']}", style={'margin': '0', 'color': '#dc3545'}),
                        html.P(f"${worst_performer['price']:.2f}", style={'margin': '5px 0', 'fontSize': '18px', 'fontWeight': 'bold'}),
                        html.P(f"{worst_performer['change_percent']:.2f}%", style={'margin': '0', 'color': '#dc3545', 'fontWeight': 'bold'})
                    ], style={
                        'border': '1px solid #dc3545',
                        'borderRadius': '8px',
                        'padding': '15px',
                        'margin': '10px',
                        'backgroundColor': '#f8d7da',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'width': '180px',
                        'display': 'inline-block',
                        'verticalAlign': 'top'
                    }),
                    
                    # Trading Volume Card
                    html.Div([
                        html.H4("Trading Volume", style={'margin': '0 0 10px 0', 'color': '#333'}),
                        html.P(f"{total_volume:,}", style={'margin': '5px 0', 'fontSize': '16px', 'fontWeight': 'bold'}),
                        html.P("Total Shares", style={'margin': '0', 'fontSize': '12px', 'color': '#666'}),
                        html.P(f"Avg: {total_volume/total_stocks:,.0f}", style={'margin': '5px 0 0 0', 'fontSize': '12px', 'color': '#666'})
                    ], style={
                        'border': '1px solid #17a2b8',
                        'borderRadius': '8px',
                        'padding': '15px',
                        'margin': '10px',
                        'backgroundColor': '#d1ecf1',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'width': '180px',
                        'display': 'inline-block',
                        'verticalAlign': 'top'
                    })
                ]
                
                market_summary_cards = summary_cards
            
            # Create current prices cards
            price_cards = []
            if not latest_df.empty:
                for _, row in latest_df.iterrows():
                    color = '#28a745' if row['change_percent'] >= 0 else '#dc3545'
                    arrow = '↑' if row['change_percent'] >= 0 else '↓'
                    
                    card = html.Div([
                        html.H3(f"{arrow} {row['symbol']}", style={'margin': '0', 'color': '#333'}),
                        html.H2(f"${row['price']:.2f}", style={'margin': '5px 0', 'color': color}),
                        html.P(f"{row['change_percent']:+.2f}%", style={'margin': '0', 'color': color, 'fontWeight': 'bold'}),
                        html.P(f"Vol: {row['volume']:,}", style={'margin': '0', 'fontSize': '12px', 'color': '#666'})
                    ], style={
                        'border': '1px solid #ddd',
                        'borderRadius': '8px',
                        'padding': '15px',
                        'margin': '10px',
                        'backgroundColor': '#f8f9fa',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'width': '180px',
                        'display': 'inline-block',
                        'textAlign': 'center'
                    })
                    price_cards.append(card)
            
            # Create price trends chart
            trends_fig = go.Figure()
            if not price_history.empty:
                for symbol in price_history['symbol'].unique():
                    symbol_data = price_history[price_history['symbol'] == symbol]
                    trends_fig.add_trace(go.Scatter(
                        x=symbol_data['timestamp'],
                        y=symbol_data['price'],
                        mode='lines+markers',
                        name=symbol,
                        line=dict(width=3),
                        hovertemplate=f'<b>{symbol}</b><br>Price: $%{{y:.2f}}<br>Time: %{{x}}<extra></extra>'
                    ))
            
            trends_fig.update_layout(
                title="Stock Price Trends Over Time",
                xaxis_title="Time",
                yaxis_title="Price ($)",
                hovermode='x unified',
                showlegend=True,
                height=400,
                template='plotly_white'
            )
            
            # Create performance comparison chart
            performance_fig = go.Figure()
            if not latest_df.empty:
                colors = ['#28a745' if x >= 0 else '#dc3545' for x in latest_df['change_percent']]
                performance_fig.add_trace(go.Bar(
                    x=latest_df['symbol'],
                    y=latest_df['change_percent'],
                    marker_color=colors,
                    text=[f"{x:+.2f}%" for x in latest_df['change_percent']],
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Change: %{y:.2f}%<extra></extra>'
                ))
            
            performance_fig.update_layout(
                title="Current Performance (% Change)",
                xaxis_title="Stock Symbol",
                yaxis_title="Change (%)",
                height=400,
                template='plotly_white',
                showlegend=False
            )
            
            # Create crypto cards
            crypto_cards = []
            if not crypto_df.empty:
                latest_crypto = crypto_df.iloc[0]  # Get most recent
                crypto_cards.append(
                    html.Div([
                        html.H3(f"BTC {latest_crypto['from_currency']}/USD", style={'margin': '0', 'color': '#333'}),
                        html.H2(f"${latest_crypto['exchange_rate']:,.2f}", style={'margin': '5px 0', 'color': '#f39c12'}),
                        html.P(f"Bid: ${latest_crypto['bid_price']:,.2f}", style={'margin': '0', 'fontSize': '12px', 'color': '#666'}),
                        html.P(f"Ask: ${latest_crypto['ask_price']:,.2f}", style={'margin': '0', 'fontSize': '12px', 'color': '#666'})
                    ], style={
                        'border': '1px solid #ddd',
                        'borderRadius': '8px',
                        'padding': '15px',
                        'margin': '10px',
                        'backgroundColor': '#fff3cd',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'width': '200px',
                        'display': 'inline-block',
                        'textAlign': 'center'
                    })
                )
            
            return market_summary_cards, price_cards, trends_fig, performance_fig, crypto_cards
    
    def run(self, debug=True, port=8050):
        """Run the dashboard"""
        print(f"Starting Financial Dashboard...")
        print(f" Dashboard will be available at: http://localhost:{port}")
        print(f" Auto-refreshing every 30 seconds")
        print(f" Press Ctrl+C to stop")
        
        self.app.run_server(debug=debug, port=port, host='0.0.0.0')

def main():
    """Main function to run the dashboard"""
    dashboard = FinancialDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
