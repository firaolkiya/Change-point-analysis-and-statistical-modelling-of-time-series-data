#!/bin/bash

# Dashboard Starter Script
# Task 3: Interactive Dashboard for Brent Oil Price Analysis
# This script starts both the Flask backend and React frontend simultaneously.

echo "============================================================"
echo "🛢️ Brent Oil Price Analysis Dashboard"
echo "Starting Backend + Frontend"
echo "============================================================"

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Stopping dashboard services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✓ Services stopped. Goodbye!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️ Virtual environment not detected. Please activate it first:"
    echo "   source venv/bin/activate"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "============================================================"
echo "🚀 STARTING DASHBOARD SERVICES"
echo "============================================================"

# Start Flask backend in background
echo "🚀 Starting Flask backend API..."
python src/dashboard_api.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to be ready..."
sleep 5

# Check if backend is running
if curl -s http://localhost:5000/api/stats > /dev/null; then
    echo "✓ Backend is ready!"
else
    echo "⚠️ Backend may not be ready yet, but continuing..."
fi

# Start React frontend in background
echo "🎨 Starting React frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 3

echo ""
echo "============================================================"
echo "✅ DASHBOARD SERVICES STARTED"
echo "============================================================"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:5000"
echo ""
echo "📋 Services running:"
echo "   • Flask Backend API (Port 5000) - PID: $BACKEND_PID"
echo "   • React Frontend (Port 3000) - PID: $FRONTEND_PID"
echo ""
echo "🛑 To stop all services, press Ctrl+C"
echo ""

# Open browser
sleep 2
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000 &
elif command -v open &> /dev/null; then
    open http://localhost:3000 &
elif command -v start &> /dev/null; then
    start http://localhost:3000 &
else
    echo "🌐 Please manually open: http://localhost:3000"
fi

# Keep script running
wait 