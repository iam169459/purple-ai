#!/bin/bash

# Purple AI - Run Script (Single Instance)
# Ensures only one instance runs at a time

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
MAIN_SCRIPT="$PROJECT_DIR/main.py"
REQ_FILE="$PROJECT_DIR/requirements.txt"
LOCK_FILE="/tmp/purple_ai.lock"
PID_FILE="/tmp/purple_ai.pid"

# Check if already running
check_single_instance() {
    if [ -f "$LOCK_FILE" ]; then
        if [ -f "$PID_FILE" ]; then
            OLD_PID=$(cat "$PID_FILE")
            if kill -0 "$OLD_PID" 2>/dev/null; then
                echo -e "${YELLOW}Purple AI is already running (PID: $OLD_PID)${NC}"
                echo -e "${BLUE}Use './run.sh stop' to stop it first${NC}"
                exit 1
            else
                echo -e "${YELLOW}Removing stale lock file...${NC}"
                rm -f "$LOCK_FILE" "$PID_FILE"
            fi
        else
            rm -f "$LOCK_FILE"
        fi
    fi
}

# Create lock file
create_lock() {
    echo $$ > "$PID_FILE"
    touch "$LOCK_FILE"
}

# Remove lock file
remove_lock() {
    rm -f "$LOCK_FILE" "$PID_FILE"
}

# Stop running instance
stop_instance() {
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo -e "${YELLOW}Stopping Purple AI (PID: $OLD_PID)...${NC}"
            kill "$OLD_PID" 2>/dev/null || true
            sleep 1
            echo -e "${GREEN}Stopped!${NC}"
        else
            echo -e "${YELLOW}No running instance found${NC}"
        fi
        remove_lock
    else
        echo -e "${YELLOW}No running instance found${NC}"
        rm -f "$LOCK_FILE"
    fi
}

# Check Python
check_python() {
    if command -v python3 &>/dev/null; then
        PYTHON="python3"
    elif command -v python &>/dev/null; then
        PYTHON="python"
    else
        echo -e "${RED}Error: Python not found${NC}"
        exit 1
    fi
}

# Setup virtual environment
setup_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        $PYTHON -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        pip install --upgrade pip -q
        if [ -f "$REQ_FILE" ]; then
            pip install -r "$REQ_FILE" -q
        fi
        echo -e "${GREEN}Virtual environment created!${NC}"
    fi
}

# Activate venv
activate_venv() {
    source "$VENV_DIR/bin/activate"
}

# Clean function
clean() {
    echo -e "${YELLOW}Cleaning...${NC}"
    remove_lock
    rm -f "$PROJECT_DIR"/*.pyc
    rm -rf "$PROJECT_DIR"/__pycache__
    rm -rf "$PROJECT_DIR"/utils/__pycache__
    rm -rf "$PROJECT_DIR"/core/__pycache__
    rm -rf "$PROJECT_DIR"/voice/__pycache__
    echo -e "${GREEN}Cleaned!${NC}"
}

# Diagnostics function
diagnose() {
    check_python
    setup_venv
    activate_venv
    echo -e "${BLUE}Running diagnostics...${NC}"
    cd "$PROJECT_DIR"
    $PYTHON -c "
import sys
sys.path.insert(0, '.')
from utils.self_repair import self_repair
results = self_repair.run_diagnostics()
print(f'Healthy: {results[\"healthy\"]}')
"
}

# Cleanup on exit
cleanup() {
    remove_lock
}
trap cleanup EXIT

# Main execution
main() {
    check_python
    
    # Handle arguments
    case "${1:-}" in
        stop)
            stop_instance
            exit 0
            ;;
        clean)
            clean
            exit 0
            ;;
        diagnose|diag)
            diagnose
            exit 0
            ;;
        --help|-h)
            echo -e "${PURPLE}Purple AI - Run Script (Single Instance)${NC}"
            echo ""
            echo "Usage: ./run.sh [option]"
            echo ""
            echo "Options:"
            echo "  (no args)    Run Purple AI"
            echo "  stop         Stop running instance"
            echo "  clean        Clean temporary files"
            echo "  diagnose     Run system diagnostics"
            echo "  --help       Show this help"
            exit 0
            ;;
    esac
    
    # Check single instance
    check_single_instance
    
    # Setup and run
    setup_venv
    activate_venv
    
    # Create lock
    create_lock
    
    cd "$PROJECT_DIR"
    exec $PYTHON "$MAIN_SCRIPT" "$@"
}

main "$@"
