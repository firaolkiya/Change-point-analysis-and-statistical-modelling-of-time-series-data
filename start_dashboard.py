#!/usr/bin/env python3
"""
Dashboard Starter Script
Task 3: Interactive Dashboard for Brent Oil Price Analysis

This script starts both the Flask backend and React frontend simultaneously.
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path
import webbrowser

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
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
    """Install frontend dependencies if needed"""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("✗ Frontend directory not found")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            os.chdir(frontend_dir)
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            os.chdir("..")
            
            if result.returncode == 0:
                print("✓ Frontend dependencies installed successfully")
                return True
            else:
                print(f"✗ Failed to install frontend dependencies: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Error installing frontend dependencies: {e}")
            os.chdir("..")
            return False
    else:
        print("✓ Frontend dependencies already installed")
        return True

def start_backend():
    """Start the Flask backend API"""
    print("🚀 Starting Flask backend API...")
    
    try:
        # Import and run the Flask app
        sys.path.append('src')
        from dashboard_api import app
        
        print("✓ Flask backend starting on http://localhost:5000")
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
        
    except Exception as e:
        print(f"✗ Error starting backend: {e}")

def start_frontend():
    """Start the React frontend"""
    print("🎨 Starting React frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("✗ Frontend directory not found")
        return
    
    try:
        os.chdir(frontend_dir)
        print("✓ React frontend starting on http://localhost:3000")
        
        # Start the React development server
        subprocess.run(['npm', 'start'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error starting frontend: {e}")
    except Exception as e:
        print(f"✗ Error starting frontend: {e}")
    finally:
        os.chdir("..")

def wait_for_backend():
    """Wait for backend to be ready"""
    import requests
    max_attempts = 30
    attempt = 0
    
    print("⏳ Waiting for backend to be ready...")
    while attempt < max_attempts:
        try:
            response = requests.get("http://localhost:5000/api/stats", timeout=2)
            if response.status_code == 200:
                print("✓ Backend is ready!")
                return True
        except:
            pass
        
        attempt += 1
        time.sleep(1)
        if attempt % 5 == 0:
            print(f"   Still waiting... ({attempt}/{max_attempts})")
    
    print("⚠️ Backend may not be ready yet, but continuing...")
    return False

def open_browser():
    """Open browser to dashboard"""
    time.sleep(3)  # Wait a bit for services to start
    try:
        webbrowser.open("http://localhost:3000")
        print("🌐 Opening dashboard in browser...")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("   Please manually open: http://localhost:3000")

def main():
    """Main function to start both services"""
    print("=" * 60)
    print("🛢️ Brent Oil Price Analysis Dashboard")
    print("Starting Backend + Frontend")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        return
    
    # Install frontend dependencies if needed
    if not install_frontend_dependencies():
        print("\n❌ Please fix frontend dependencies and try again.")
        return
    
    print("\n" + "=" * 60)
    print("🚀 STARTING DASHBOARD SERVICES")
    print("=" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Wait for backend to be ready
    wait_for_backend()
    
    # Start frontend in a separate thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    # Open browser after a short delay
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n" + "=" * 60)
    print("✅ DASHBOARD SERVICES STARTED")
    print("=" * 60)
    print("🌐 Frontend: http://localhost:3000")
    print("🔌 Backend API: http://localhost:5000")
    print("\n📋 Services running:")
    print("   • Flask Backend API (Port 5000)")
    print("   • React Frontend (Port 3000)")
    print("\n🛑 To stop all services, press Ctrl+C")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping dashboard services...")
        print("✓ Services stopped. Goodbye!")

if __name__ == "__main__":
    main() 