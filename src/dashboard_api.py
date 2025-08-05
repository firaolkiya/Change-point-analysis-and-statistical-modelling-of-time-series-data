"""
Flask API Backend for Brent Oil Price Analysis Dashboard
Task 3: Interactive Dashboard Application

This module provides RESTful APIs to serve analysis results and data
for the React frontend dashboard.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os
import sys

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our analysis modules
from time_series_analysis import BrentOilAnalyzer
from bayesian_change_point import BayesianChangePointAnalyzer

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend
api = Api(app)

class DataManager:
    """Manages data loading and processing for the dashboard"""
    
    def __init__(self):
        self.price_data = None
        self.events_data = None
        self.change_points = None
        self.regime_analysis = None
        self.load_data()
    
    def load_data(self):
        """Load all required data for the dashboard"""
        try:
            # Load price data
            analyzer = BrentOilAnalyzer('data/BrentOilPrices.csv')
            analyzer.load_data()
            analyzer.preprocess_data()
            
            self.price_data = analyzer.df_processed.reset_index()
            self.price_data['Date'] = self.price_data['Date'].dt.strftime('%Y-%m-%d')
            
            # Load events data
            self.events_data = pd.read_csv('data/major_oil_events.csv')
            self.events_data['Date'] = pd.to_datetime(self.events_data['Date'])
            self.events_data['Date'] = self.events_data['Date'].dt.strftime('%Y-%m-%d')
            
            # Load change point analysis results if available
            self.load_analysis_results()
            
            print("✓ Data loaded successfully for dashboard")
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def load_analysis_results(self):
        """Load analysis results from output files"""
        try:
            # Try to load change point analysis results
            if os.path.exists('output/bayesian_change_point_report.txt'):
                # Parse the report to extract change points
                self.change_points = self.parse_change_point_report()
            
            # Load regime analysis if available
            if hasattr(self, 'change_points') and self.change_points:
                self.regime_analysis = self.generate_regime_analysis()
                
        except Exception as e:
            print(f"Error loading analysis results: {e}")
    
    def parse_change_point_report(self):
        """Parse the change point analysis report"""
        change_points = []
        try:
            with open('output/bayesian_change_point_report.txt', 'r') as f:
                content = f.read()
                
            # Extract change point information
            lines = content.split('\n')
            current_cp = None
            
            for line in lines:
                if line.startswith('Change Point'):
                    if current_cp:
                        change_points.append(current_cp)
                    current_cp = {'name': line.strip()}
                elif current_cp and line.strip().startswith('Date:'):
                    current_cp['date'] = line.split(':')[1].strip()
                elif current_cp and line.strip().startswith('Confidence Interval:'):
                    interval = line.split(':')[1].strip()
                    current_cp['confidence_interval'] = interval
                elif current_cp and line.strip().startswith('Uncertainty:'):
                    uncertainty = line.split(':')[1].strip()
                    current_cp['uncertainty'] = uncertainty
            
            if current_cp:
                change_points.append(current_cp)
                
        except Exception as e:
            print(f"Error parsing change point report: {e}")
        
        return change_points
    
    def generate_regime_analysis(self):
        """Generate regime analysis from change points"""
        if not self.change_points:
            return []
        
        regimes = []
        price_data = self.price_data.copy()
        price_data['Date'] = pd.to_datetime(price_data['Date'])
        
        # Sort change points by date
        sorted_cps = sorted(self.change_points, key=lambda x: x.get('date', ''))
        
        for i, cp in enumerate(sorted_cps):
            cp_date = pd.to_datetime(cp['date'])
            
            if i == 0:
                # First regime: from start to first change point
                start_date = price_data['Date'].min()
                end_date = cp_date
            else:
                # Middle regimes: from previous change point to current
                start_date = pd.to_datetime(sorted_cps[i-1]['date'])
                end_date = cp_date
            
            # Calculate regime statistics
            regime_data = price_data[
                (price_data['Date'] >= start_date) & 
                (price_data['Date'] < end_date)
            ]
            
            if len(regime_data) > 0:
                regime = {
                    'regime_id': i,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'duration_days': (end_date - start_date).days,
                    'mean_price': float(regime_data['Price'].mean()),
                    'std_price': float(regime_data['Price'].std()),
                    'min_price': float(regime_data['Price'].min()),
                    'max_price': float(regime_data['Price'].max()),
                    'change_point': cp['date']
                }
                regimes.append(regime)
        
        # Add final regime
        if sorted_cps:
            last_cp_date = pd.to_datetime(sorted_cps[-1]['date'])
            final_regime_data = price_data[price_data['Date'] >= last_cp_date]
            
            if len(final_regime_data) > 0:
                final_regime = {
                    'regime_id': len(sorted_cps),
                    'start_date': last_cp_date.strftime('%Y-%m-%d'),
                    'end_date': price_data['Date'].max().strftime('%Y-%m-%d'),
                    'duration_days': (price_data['Date'].max() - last_cp_date).days,
                    'mean_price': float(final_regime_data['Price'].mean()),
                    'std_price': float(final_regime_data['Price'].std()),
                    'min_price': float(final_regime_data['Price'].min()),
                    'max_price': float(final_regime_data['Price'].max()),
                    'change_point': None
                }
                regimes.append(final_regime)
        
        return regimes

# Initialize data manager
data_manager = DataManager()

class PriceDataAPI(Resource):
    """API endpoint for price data"""
    
    def get(self):
        """Get price data with optional filtering"""
        try:
            # Get query parameters
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            limit = request.args.get('limit', type=int)
            
            data = data_manager.price_data.copy()
            
            # Apply date filters
            if start_date:
                data = data[data['Date'] >= start_date]
            if end_date:
                data = data[data['Date'] <= end_date]
            
            # Apply limit
            if limit:
                data = data.tail(limit)
            
            # Convert to JSON-serializable format
            result = {
                'data': data.to_dict('records'),
                'total_records': len(data),
                'date_range': {
                    'start': data['Date'].min() if len(data) > 0 else None,
                    'end': data['Date'].max() if len(data) > 0 else None
                }
            }
            
            return jsonify(result)
            
        except Exception as e:
            return {'error': str(e)}, 500

class EventsDataAPI(Resource):
    """API endpoint for events data"""
    
    def get(self):
        """Get events data with optional filtering"""
        try:
            # Get query parameters
            category = request.args.get('category')
            impact_direction = request.args.get('impact_direction')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            data = data_manager.events_data.copy()
            
            # Apply filters
            if category:
                data = data[data['Event_Category'] == category]
            if impact_direction:
                data = data[data['Impact_Direction'] == impact_direction]
            if start_date:
                data = data[data['Date'] >= start_date]
            if end_date:
                data = data[data['Date'] <= end_date]
            
            # Get unique categories and impact directions for filters
            categories = data_manager.events_data['Event_Category'].unique().tolist()
            impact_directions = data_manager.events_data['Impact_Direction'].unique().tolist()
            
            result = {
                'data': data.to_dict('records'),
                'total_events': len(data),
                'filters': {
                    'categories': categories,
                    'impact_directions': impact_directions
                }
            }
            
            return jsonify(result)
            
        except Exception as e:
            return {'error': str(e)}, 500

class ChangePointsAPI(Resource):
    """API endpoint for change point analysis results"""
    
    def get(self):
        """Get change point analysis results"""
        try:
            result = {
                'change_points': data_manager.change_points or [],
                'regime_analysis': data_manager.regime_analysis or [],
                'total_change_points': len(data_manager.change_points) if data_manager.change_points else 0
            }
            
            return jsonify(result)
            
        except Exception as e:
            return {'error': str(e)}, 500

class EventImpactAPI(Resource):
    """API endpoint for event impact analysis"""
    
    def get(self):
        """Analyze impact of events on oil prices"""
        try:
            event_id = request.args.get('event_id')
            window_days = request.args.get('window_days', 30, type=int)
            
            if not event_id:
                return {'error': 'event_id parameter required'}, 400
            
            # Find the event
            event = data_manager.events_data.iloc[int(event_id)] if event_id.isdigit() else None
            
            if event is None:
                return {'error': 'Event not found'}, 404
            
            event_date = pd.to_datetime(event['Date'])
            
            # Get price data around the event
            price_data = data_manager.price_data.copy()
            price_data['Date'] = pd.to_datetime(price_data['Date'])
            
            # Calculate window
            start_date = event_date - timedelta(days=window_days)
            end_date = event_date + timedelta(days=window_days)
            
            # Get data in window
            window_data = price_data[
                (price_data['Date'] >= start_date) & 
                (price_data['Date'] <= end_date)
            ].copy()
            
            if len(window_data) == 0:
                return {'error': 'No price data available for this period'}, 404
            
            # Calculate impact metrics
            pre_event = window_data[window_data['Date'] < event_date]
            post_event = window_data[window_data['Date'] >= event_date]
            
            impact_analysis = {
                'event': event.to_dict(),
                'window_days': window_days,
                'pre_event': {
                    'mean_price': float(pre_event['Price'].mean()) if len(pre_event) > 0 else None,
                    'std_price': float(pre_event['Price'].std()) if len(pre_event) > 0 else None,
                    'data_points': len(pre_event)
                },
                'post_event': {
                    'mean_price': float(post_event['Price'].mean()) if len(post_event) > 0 else None,
                    'std_price': float(post_event['Price'].std()) if len(post_event) > 0 else None,
                    'data_points': len(post_event)
                },
                'price_change': {
                    'absolute': float(post_event['Price'].mean() - pre_event['Price'].mean()) if len(pre_event) > 0 and len(post_event) > 0 else None,
                    'percentage': float(((post_event['Price'].mean() - pre_event['Price'].mean()) / pre_event['Price'].mean()) * 100) if len(pre_event) > 0 and len(post_event) > 0 else None
                },
                'window_data': window_data.to_dict('records')
            }
            
            return jsonify(impact_analysis)
            
        except Exception as e:
            return {'error': str(e)}, 500

class DashboardStatsAPI(Resource):
    """API endpoint for dashboard statistics"""
    
    def get(self):
        """Get overall dashboard statistics"""
        try:
            price_data = data_manager.price_data
            events_data = data_manager.events_data
            
            # Calculate basic statistics
            stats = {
                'price_data': {
                    'total_records': len(price_data),
                    'date_range': {
                        'start': price_data['Date'].min(),
                        'end': price_data['Date'].max()
                    },
                    'price_stats': {
                        'mean': float(price_data['Price'].mean()),
                        'std': float(price_data['Price'].std()),
                        'min': float(price_data['Price'].min()),
                        'max': float(price_data['Price'].max())
                    }
                },
                'events_data': {
                    'total_events': len(events_data),
                    'categories': events_data['Event_Category'].value_counts().to_dict(),
                    'impact_directions': events_data['Impact_Direction'].value_counts().to_dict()
                },
                'analysis_results': {
                    'change_points_count': len(data_manager.change_points) if data_manager.change_points else 0,
                    'regimes_count': len(data_manager.regime_analysis) if data_manager.regime_analysis else 0
                }
            }
            
            return jsonify(stats)
            
        except Exception as e:
            return {'error': str(e)}, 500

# Register API endpoints
api.add_resource(PriceDataAPI, '/api/price-data')
api.add_resource(EventsDataAPI, '/api/events')
api.add_resource(ChangePointsAPI, '/api/change-points')
api.add_resource(EventImpactAPI, '/api/event-impact')
api.add_resource(DashboardStatsAPI, '/api/stats')

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Brent Oil Price Analysis Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .api-info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .endpoint { background: #e9ecef; padding: 10px; margin: 10px 0; border-radius: 3px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛢️ Brent Oil Price Analysis Dashboard</h1>
            <p>Welcome to the Brent Oil Price Analysis Dashboard API. This backend serves data for the React frontend.</p>
            
            <div class="api-info">
                <h3>Available API Endpoints:</h3>
                <div class="endpoint">GET /api/price-data - Get Brent oil price data</div>
                <div class="endpoint">GET /api/events - Get major oil events data</div>
                <div class="endpoint">GET /api/change-points - Get change point analysis results</div>
                <div class="endpoint">GET /api/event-impact?event_id=X - Analyze event impact</div>
                <div class="endpoint">GET /api/stats - Get dashboard statistics</div>
            </div>
            
            <p><strong>Frontend:</strong> The React frontend should be running on a different port and will consume these APIs.</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("Starting Brent Oil Price Analysis Dashboard API...")
    print("API will be available at: http://localhost:5000")
    print("Frontend should be running on: http://localhost:3000")
    app.run(debug=True, host='0.0.0.0', port=5000) 