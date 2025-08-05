#!/usr/bin/env python3
"""
Simple Dashboard Starter
Task 3: Interactive Dashboard for Brent Oil Price Analysis

This script starts both the Flask backend and React frontend using concurrent.futures.
"""

import subprocess
import time
import signal
import sys
import os
from pathlib import Path
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_backend_ready():
    """Check if backend is ready"""
    try:
        import requests
        response = requests.get("http://localhost:5000/api/stats", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start Flask backend"""
    print("🚀 Starting Flask backend...")
    try:
        # Change to project root
        os.chdir(Path(__file__).parent)
        
        # Start Flask app using virtual environment
        venv_python = Path("venv/bin/python")
        if venv_python.exists():
            process = subprocess.Popen([
                str(venv_python), "src/dashboard_api.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            # Fallback to system Python
            process = subprocess.Popen([
                sys.executable, "src/dashboard_api.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for backend to be ready
        for i in range(30):
            if check_backend_ready():
                print("✓ Backend is ready!")
                return process
            time.sleep(1)
            if i % 5 == 0:
                print(f"   Waiting for backend... ({i}/30)")
        
        print("⚠️ Backend may not be ready yet")
        return process
        
    except Exception as e:
        print(f"✗ Error starting backend: {e}")
        return None

def start_frontend():
    """Start React frontend"""
    print("🎨 Starting React frontend...")
    try:
        # Change to frontend directory
        frontend_dir = Path("frontend")
        os.chdir(frontend_dir)
        
        # Start React dev server
        process = subprocess.Popen([
            "npm", "start"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for frontend to start
        time.sleep(5)
        print("✓ Frontend started!")
        
        # Change back to project root
        os.chdir("..")
        return process
        
    except Exception as e:
        print(f"✗ Error starting frontend: {e}")
        os.chdir("..")
        return None

def open_browser():
    """Open browser to dashboard"""
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:3000")
        print("🌐 Opening dashboard in browser...")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("   Please manually open: http://localhost:3000")

def main():
    """Main function"""
    print("=" * 60)
    print("🛢️ Brent Oil Price Analysis Dashboard")
    print("Starting Both Services")
    print("=" * 60)
    
    # Check dependencies
    try:
        import flask
        print("✓ Flask available")
    except ImportError:
        print("❌ Flask not installed. Run: pip install -r requirements.txt")
        return
    
    # Check if Node.js is available
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        print("✓ Node.js available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js not installed")
        return
    
    # Check if frontend dependencies are installed
    if not Path("frontend/node_modules").exists():
        print("📦 Installing frontend dependencies...")
        try:
            os.chdir("frontend")
            subprocess.run(["npm", "install"], check=True)
            os.chdir("..")
            print("✓ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return
    
    print("\n🚀 Starting services...")
    
    processes = []
    
    # Start backend
    backend_process = start_backend()
    if backend_process:
        processes.append(("Backend", backend_process))
    
    # Start frontend
    frontend_process = start_frontend()
    if frontend_process:
        processes.append(("Frontend", frontend_process))
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n" + "=" * 60)
    print("✅ DASHBOARD SERVICES STARTED")
    print("=" * 60)
    print("🌐 Frontend: http://localhost:3000")
    print("🔌 Backend API: http://localhost:5000")
    print("\n🛑 To stop all services, press Ctrl+C")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            for name, process in processes:
                if process.poll() is not None:
                    print(f"⚠️ {name} process stopped unexpectedly")
                    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping services...")
        
        # Stop all processes
        for name, process in processes:
            if process and process.poll() is None:
                print(f"   Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✓ All services stopped. Goodbye!")

if __name__ == "__main__":
    import threading
    main() 