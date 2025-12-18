#!/bin/bash

# Edu2Job - One-Command Startup Script
# Installs dependencies, trains ML model, and starts the complete application

echo "🚀 Starting Edu2Job Complete Setup..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Step 1: Check Python version
echo -e "${BLUE}🐍 Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ $PYTHON_VERSION found${NC}"
echo ""

# Step 2: Install Python dependencies (system-wide or venv)
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
if [ -f "ml/requirements.txt" ]; then
    python3 -m pip install -q -r ml/requirements.txt
    echo -e "${GREEN}✓ ML dependencies installed${NC}"
fi
if [ -f "requirements.txt" ]; then
    python3 -m pip install -q -r requirements.txt
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
fi
echo ""

# Step 3: Check if ML model exists
echo -e "${BLUE}🤖 Checking ML model...${NC}"
if [ ! -f "backend/models/best_model.pkl" ]; then
    echo -e "${YELLOW}⚠️  ML model not found. Training now...${NC}"
    echo -e "${BLUE}   This will take 5-10 minutes...${NC}"
    echo ""
    
    cd ml
    python3 model_training.py
    TRAIN_EXIT=$?
    cd ..
    
    if [ $TRAIN_EXIT -ne 0 ]; then
        echo -e "${RED}❌ Model training failed!${NC}"
        echo -e "${YELLOW}Check logs for details. You can continue without ML predictions.${NC}"
        echo ""
    else
        # Move trained models to backend/models
        mv best_model.pkl preprocessor.pkl label_encoders.pkl scaler.pkl backend/models/ 2>/dev/null
        echo -e "${GREEN}✓ Model trained and moved to backend/models/${NC}"
        echo ""
    fi
else
    echo -e "${GREEN}✓ ML model found (backend/models/best_model.pkl)${NC}"
    echo ""
fi

# Step 4: Check if port 8000 is already in use
echo -e "${BLUE}🔍 Checking port 8000...${NC}"
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use${NC}"
    echo "Stopping existing process..."
    lsof -ti :8000 | xargs kill -9 2>/dev/null
    sleep 1
    echo -e "${GREEN}✓ Port 8000 cleared${NC}"
else
    echo -e "${GREEN}✓ Port 8000 available${NC}"
fi
echo ""

# Step 5: Start the backend server
echo -e "${BLUE}� Starting Flask backend server...${NC}"
cd backend

# Start server and capture PID
python3 app.py > ../logs/server_output.log 2>&1 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Check if server is running
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend server started successfully${NC}"
    echo -e "${GREEN}  Server PID: $SERVER_PID${NC}"
    echo -e "${GREEN}  Running on: http://localhost:8000${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠️  Server failed to start. Check logs/server_output.log for details${NC}"
    exit 1
fi

# Go back to root directory
cd ..

# Save PID to file for easy stopping later
echo $SERVER_PID > .server_pid

# Open frontend in default browser
echo -e "${BLUE}🌐 Opening frontend in browser...${NC}"
sleep 1

# Detect OS and open browser accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "frontend/login.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "frontend/login.html" 2>/dev/null
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    start "frontend/login.html"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         ✨ Edu2Job is Now Running! ✨         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📍 Backend API:${NC}      http://localhost:8000"
echo -e "${BLUE}📍 Frontend:${NC}         frontend/login.html (opened in browser)"
if [ -f "backend/models/best_model.pkl" ]; then
    echo -e "${BLUE}🤖 ML Model:${NC}         ✓ Loaded and ready"
else
    echo -e "${BLUE}🤖 ML Model:${NC}         ⚠️  Not available (predictions will use fallback)"
fi
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}To stop the server:${NC}"
echo -e "  ${BLUE}./stop.sh${NC}  or  ${BLUE}Ctrl+C${NC}"
echo ""
echo -e "${BLUE}Logs:${NC} logs/server_output.log"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}🎯 Happy job matching!${NC}"
echo ""

# Keep script running to show logs (optional)
echo -e "${BLUE}Press Ctrl+C to stop the server...${NC}"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping server...'; kill $SERVER_PID 2>/dev/null; rm -f .server_pid; echo 'Server stopped.'; exit 0" INT TERM

# Keep the script running and show live logs
tail -f logs/server_output.log 2>/dev/null &
wait $SERVER_PID
