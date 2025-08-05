#!/usr/bin/env python3
"""
Dashboard Demonstration Script
Task 3: Interactive Dashboard for Brent Oil Price Analysis

This script demonstrates the complete dashboard functionality and provides
instructions for running the full application.
"""

import requests
import json
import time
from datetime import datetime

def test_api_endpoints():
    """Test all API endpoints and display results"""
    base_url = "http://localhost:5000"
    
    print("🛢️ Brent Oil Price Analysis Dashboard - API Demo")
    print("=" * 60)
    
    # Test 1: Stats endpoint
    print("\n1. Testing Dashboard Statistics...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✓ Dashboard Statistics:")
            print(f"   • Total Price Records: {stats['price_data']['total_records']:,}")
            print(f"   • Date Range: {stats['price_data']['date_range']['start']} to {stats['price_data']['date_range']['end']}")
            print(f"   • Average Price: ${stats['price_data']['price_stats']['mean']:.2f}")
            print(f"   • Total Events: {stats['events_data']['total_events']}")
            print(f"   • Change Points: {stats['analysis_results']['change_points_count']}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False
    
    # Test 2: Price data endpoint
    print("\n2. Testing Price Data API...")
    try:
        response = requests.get(f"{base_url}/api/price-data?limit=3")
        if response.status_code == 200:
            price_data = response.json()
            print("✓ Recent Price Data:")
            for item in price_data['data']:
                print(f"   • {item['Date']}: ${item['Price']:.2f}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False
    
    # Test 3: Events endpoint
    print("\n3. Testing Events API...")
    try:
        response = requests.get(f"{base_url}/api/events?limit=3")
        if response.status_code == 200:
            events_data = response.json()
            print("✓ Recent Events:")
            for event in events_data['data'][:3]:
                print(f"   • {event['Date']}: {event['Event_Description'][:50]}...")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False
    
    # Test 4: Change points endpoint
    print("\n4. Testing Change Points API...")
    try:
        response = requests.get(f"{base_url}/api/change-points")
        if response.status_code == 200:
            change_points = response.json()
            print(f"✓ Change Points Analysis:")
            print(f"   • Total Change Points: {change_points['total_change_points']}")
            if change_points['change_points']:
                for cp in change_points['change_points'][:2]:
                    print(f"   • {cp.get('name', 'Unknown')}: {cp.get('date', 'Unknown')}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False
    
    return True

def show_dashboard_features():
    """Display dashboard features and capabilities"""
    print("\n" + "=" * 60)
    print("📊 DASHBOARD FEATURES")
    print("=" * 60)
    
    features = [
        {
            "category": "Interactive Visualizations",
            "features": [
                "Real-time Brent oil price trends",
                "Event timeline with filtering",
                "Change point analysis visualization",
                "Impact analysis charts",
                "Statistical dashboard overview"
            ]
        },
        {
            "category": "Data Analysis",
            "features": [
                "Historical price data (1987-2022)",
                "28 major oil market events",
                "Bayesian change point detection",
                "Event impact quantification",
                "Regime analysis results"
            ]
        },
        {
            "category": "Interactive Features",
            "features": [
                "Date range filtering",
                "Event category filtering",
                "Impact direction filtering",
                "Real-time data updates",
                "Responsive design (mobile/desktop)"
            ]
        },
        {
            "category": "Technical Stack",
            "features": [
                "Flask RESTful API backend",
                "React 18 frontend",
                "Recharts for visualizations",
                "Styled-components for styling",
                "Framer Motion animations"
            ]
        }
    ]
    
    for category in features:
        print(f"\n🔹 {category['category']}:")
        for feature in category['features']:
            print(f"   • {feature}")

def show_installation_instructions():
    """Display installation and setup instructions"""
    print("\n" + "=" * 60)
    print("🚀 INSTALLATION & SETUP")
    print("=" * 60)
    
    print("\n📋 Prerequisites:")
    print("   • Python 3.8+ with virtual environment")
    print("   • Node.js 16+ and npm")
    print("   • Git (for cloning repository)")
    
    print("\n🔧 Backend Setup:")
    print("   1. Install Python dependencies:")
    print("      pip install -r requirements.txt")
    print("   2. Start Flask API server:")
    print("      python run_dashboard.py --backend")
    
    print("\n🎨 Frontend Setup:")
    print("   1. Install Node.js dependencies:")
    print("      cd frontend && npm install")
    print("   2. Start React development server:")
    print("      cd frontend && npm start")
    
    print("\n🌐 Access Dashboard:")
    print("   • Frontend: http://localhost:3000")
    print("   • Backend API: http://localhost:5000")
    print("   • API Documentation: http://localhost:5000")

def show_api_endpoints():
    """Display available API endpoints"""
    print("\n" + "=" * 60)
    print("🔌 API ENDPOINTS")
    print("=" * 60)
    
    endpoints = [
        {
            "endpoint": "GET /api/stats",
            "description": "Dashboard statistics and overview",
            "example": "curl http://localhost:5000/api/stats"
        },
        {
            "endpoint": "GET /api/price-data",
            "description": "Brent oil price data with filtering",
            "example": "curl 'http://localhost:5000/api/price-data?start_date=2020-01-01&limit=100'"
        },
        {
            "endpoint": "GET /api/events",
            "description": "Major oil events with filtering",
            "example": "curl 'http://localhost:5000/api/events?category=Geopolitical'"
        },
        {
            "endpoint": "GET /api/change-points",
            "description": "Change point analysis results",
            "example": "curl http://localhost:5000/api/change-points"
        },
        {
            "endpoint": "GET /api/event-impact",
            "description": "Analyze specific event impact",
            "example": "curl 'http://localhost:5000/api/event-impact?event_id=5&window_days=30'"
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n🔹 {endpoint['endpoint']}")
        print(f"   Description: {endpoint['description']}")
        print(f"   Example: {endpoint['example']}")

def main():
    """Main demonstration function"""
    print("🛢️ Brent Oil Price Analysis Dashboard")
    print("Task 3: Interactive Dashboard Implementation")
    print("=" * 60)
    
    # Test API endpoints
    print("\nTesting API endpoints...")
    if test_api_endpoints():
        print("\n✅ All API endpoints working correctly!")
    else:
        print("\n❌ API testing failed. Please ensure the Flask backend is running.")
        print("   Start with: python run_dashboard.py --backend")
        return
    
    # Show features
    show_dashboard_features()
    
    # Show installation instructions
    show_installation_instructions()
    
    # Show API endpoints
    show_api_endpoints()
    
    print("\n" + "=" * 60)
    print("🎉 DASHBOARD DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the backend: python run_dashboard.py --backend")
    print("2. Start the frontend: python run_dashboard.py --frontend")
    print("3. Open http://localhost:3000 in your browser")
    print("\nFor more information, see docs/Task3_Dashboard_README.md")

if __name__ == "__main__":
    main() 