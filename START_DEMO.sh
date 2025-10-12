#!/bin/bash
# Start all services for the demo

echo "=========================================="
echo "Starting Nezasa Connect Demo Environment"
echo "=========================================="
echo ""

# Kill any existing processes on the ports
echo "🧹 Cleaning up existing processes..."
pkill -f "uvicorn api:app" 2>/dev/null
pkill -f "serve_logs.py" 2>/dev/null
pkill -f "streamlit run app.py" 2>/dev/null
sleep 2

# Start API server
echo "🚀 Starting API Server (port 8000)..."
nohup python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 > api_server.log 2>&1 &
API_PID=$!
sleep 3

# Check if API is running
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "   ✅ API Server running (PID: $API_PID)"
    echo "   📍 API Docs: http://localhost:8000/api/docs"
else
    echo "   ❌ API Server failed to start"
    exit 1
fi

# Start Log Viewer Server
echo ""
echo "📊 Starting Log Viewer Server (port 8080)..."
nohup python3 serve_logs.py > log_server.log 2>&1 &
LOG_PID=$!
sleep 2

# Check if Log Viewer is running
if curl -s http://localhost:8080/ > /dev/null 2>&1; then
    echo "   ✅ Log Viewer running (PID: $LOG_PID)"
    echo "   📍 Log Viewer: http://localhost:8080/view_logs.html"
else
    echo "   ❌ Log Viewer failed to start"
fi

# Instructions for Streamlit
echo ""
echo "🎨 To start Streamlit UI:"
echo "   Run in a new terminal:"
echo "   streamlit run app.py"
echo "   📍 UI: http://localhost:8501"
echo ""

echo "=========================================="
echo "✅ Demo Environment Ready!"
echo "=========================================="
echo ""
echo "📋 Next Steps:"
echo "1. Start Streamlit: streamlit run app.py"
echo "2. Open Log Viewer: http://localhost:8080/view_logs.html"
echo "3. Open API Docs: http://localhost:8000/api/docs"
echo "4. Open Streamlit UI: http://localhost:8501"
echo ""
echo "🧪 Test API:"
echo "curl -X GET http://localhost:8000/api/v1/credentials -H 'X-API-Key: admin_key_123'"
echo ""
echo "🛑 To stop all services:"
echo "./STOP_DEMO.sh"
echo ""

