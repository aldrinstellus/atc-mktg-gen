#!/bin/bash
# Run script for ATC Marketing Asset Generator v1.0

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  ATC Marketing Asset Generator v1.0   ${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo -e "${GREEN}Created .env file. Please edit it with your API keys.${NC}"
    echo ""
fi

# Check for GOOGLE_API_KEY
if [ -z "$GOOGLE_API_KEY" ]; then
    source .env 2>/dev/null
fi

if [ -z "$GOOGLE_API_KEY" ]; then
    echo "Warning: GOOGLE_API_KEY not set. Image generation will be disabled."
    echo "Set it in .env or export GOOGLE_API_KEY=your_key"
    echo ""
fi

# Function to run locally (without Docker)
run_local() {
    echo -e "${GREEN}Starting services locally...${NC}"
    echo ""

    # Start FastAPI in background
    echo "Starting FastAPI backend on http://localhost:8000"
    cd "$(dirname "$0")"
    PYTHONPATH=. python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
    API_PID=$!

    sleep 2

    # Start Streamlit
    echo "Starting Streamlit frontend on http://localhost:8501"
    PYTHONPATH=. streamlit run src/ui/app.py --server.port 8501 &
    UI_PID=$!

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Services Running:${NC}"
    echo -e "${GREEN}  - API:      http://localhost:8000${NC}"
    echo -e "${GREEN}  - UI:       http://localhost:8501${NC}"
    echo -e "${GREEN}  - API Docs: http://localhost:8000/docs${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Press Ctrl+C to stop all services"

    # Wait for Ctrl+C
    trap "kill $API_PID $UI_PID 2>/dev/null; exit" INT
    wait
}

# Function to run with Docker
run_docker() {
    echo -e "${GREEN}Starting services with Docker...${NC}"
    docker-compose up --build
}

# Check command line argument
case "${1:-local}" in
    local)
        run_local
        ;;
    docker)
        run_docker
        ;;
    api)
        echo "Starting API only..."
        PYTHONPATH=. python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    ui)
        echo "Starting UI only..."
        PYTHONPATH=. streamlit run src/ui/app.py --server.port 8501
        ;;
    *)
        echo "Usage: ./run.sh [local|docker|api|ui]"
        echo "  local  - Run both services locally (default)"
        echo "  docker - Run with Docker Compose"
        echo "  api    - Run API only"
        echo "  ui     - Run UI only"
        ;;
esac
