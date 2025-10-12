#!/bin/bash
# Stop all demo services

echo "🛑 Stopping Nezasa Connect Demo Services..."
echo ""

pkill -f "uvicorn api:app"
pkill -f "serve_logs.py"  
pkill -f "streamlit run app.py"

sleep 2

echo "✅ All services stopped"
echo ""

