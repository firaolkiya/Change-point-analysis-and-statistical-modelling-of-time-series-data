#!/usr/bin/env python3
"""
Dashboard Runner Script
Task 3: Interactive Dashboard for Brent Oil Price Analysis

This script starts both the Flask backend API and provides instructions
for running the React frontend.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import flask_cors
        import flask_restful
        print("✓ Flask dependencies available")
    except ImportError as e:
        print(f"✗ Missing Flask dependency: {e}")
        print("  Run: pip install -r requirements.txt")
        return False
    
    # Check if Node.js is installed
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js available: {result.stdout.strip()}")
        else:
            print("✗ Node.js not found")
            return False
    except FileNotFoundError:
        print("✗ Node.js not installed")
        print("  Please install Node.js from https://nodejs.org/")
        return False
    
    # Check if npm is available
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ npm available: {result.stdout.strip()}")
        else:
            print("✗ npm not found")
            return False
    except FileNotFoundError:
        print("✗ npm not installed")
        return False
    
    return True

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("\nInstalling frontend dependencies...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("✗ Frontend directory not found")
        return False
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Install dependencies
        print("Running: npm install")
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Frontend dependencies installed successfully")
            os.chdir("..")  # Go back to root
            return True
        else:
            print(f"✗ Failed to install frontend dependencies: {result.stderr}")
            os.chdir("..")  # Go back to root
            return False
            
    except Exception as e:
        print(f"✗ Error installing frontend dependencies: {e}")
        os.chdir("..")  # Go back to root
        return False

def start_backend():
    """Start the Flask backend API"""
    print("\nStarting Flask backend API...")
    
    try:
        # Import and run the Flask app
        sys.path.append('src')
        from dashboard_api import app
        
        print("✓ Flask backend starting on http://localhost:5000")
        print("  Press Ctrl+C to stop the backend")
        
        # Start the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n✓ Backend stopped by user")
    except Exception as e:
        print(f"✗ Error starting backend: {e}")

def start_frontend():
    """Start the React frontend"""
    print("\nStarting React frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("✗ Frontend directory not found")
        return
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        print("✓ React frontend starting on http://localhost:3000")
        print("  Press Ctrl+C to stop the frontend")
        
        # Start the React development server
        subprocess.run(['npm', 'start'])
        
    except KeyboardInterrupt:
        print("\n✓ Frontend stopped by user")
    except Exception as e:
        print(f"✗ Error starting frontend: {e}")
    finally:
        os.chdir("..")  # Go back to root

def main():
    """Main function to run the dashboard"""
    print("=" * 60)
    print("🛢️ Brent Oil Price Analysis Dashboard")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        return
    
    # Install frontend dependencies if needed
    if not install_frontend_dependencies():
        print("\nPlease fix frontend dependencies and try again.")
        return
    
    print("\n" + "=" * 60)
    print("DASHBOARD SETUP COMPLETE")
    print("=" * 60)
    print("\nTo start the dashboard:")
    print("\n1. Start the backend (in one terminal):")
    print("   python run_dashboard.py --backend")
    print("\n2. Start the frontend (in another terminal):")
    print("   python run_dashboard.py --frontend")
    print("\n3. Or start both together:")
    print("   python run_dashboard.py --both")
    print("\nThe dashboard will be available at:")
    print("  Frontend: http://localhost:3000")
    print("  Backend API: http://localhost:5000")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "--backend":
            start_backend()
        elif mode == "--frontend":
            start_frontend()
        elif mode == "--both":
            print("\nStarting both backend and frontend...")
            print("Note: This will start the backend in the current terminal.")
            print("The frontend will need to be started in a separate terminal.")
            print("\nTo start frontend in another terminal, run:")
            print("  cd frontend && npm start")
            print("\nStarting backend now...")
            start_backend()
        else:
            print(f"Unknown mode: {mode}")
            print("Available modes: --backend, --frontend, --both")

if __name__ == "__main__":
    main() 