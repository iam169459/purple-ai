#!/bin/bash

# Purple AI - Run Script (Single Instance)

set -e

# Project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
MAIN_SCRIPT="$PROJECT_DIR/main.py"
REQ_FILE="$PROJECT_DIR/requirements.txt"
LOCK_FILE="/tmp/purple_ai.lock"
PID_FILE="/tmp/purple_ai.pid"

# Kill any existing purple ai processes
kill_existing() {
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "Stopping existing Purple AI (PID: $OLD_PID)..."
            kill "$OLD_PID" 2>/dev/null || true
            sleep 1
        fi
        rm -f "$PID_FILE"
    fi
    pkill -f "python.*main.py" 2>/dev/null || true
    rm -f "$LOCK_FILE"
}

# Check if already running
check_single_instance() {
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "Purple AI is already running (PID: $OLD_PID)"
            echo "Use './run.sh stop' to stop it first"
            exit 1
        else
            rm -f "$LOCK_FILE" "$PID_FILE"
        fi
    fi
    rm -f "$LOCK_FILE"
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
    kill_existing
    echo "Purple AI stopped!"
}

# Check Python
check_python() {
    if command -v python3 &>/dev/null; then
        PYTHON="python3"
    elif command -v python &>/dev/null; then
        PYTHON="python"
    else
        echo "Error: Python not found"
        exit 1
    fi
}

# Setup virtual environment
setup_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        $PYTHON -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        pip install --upgrade pip -q
        if [ -f "$REQ_FILE" ]; then
            pip install -r "$REQ_FILE" -q
        fi
        echo "Virtual environment created!"
    fi
}

# Activate venv
activate_venv() {
    source "$VENV_DIR/bin/activate"
}

# Clean function
clean() {
    echo "Cleaning..."
    kill_existing
    rm -f "$PROJECT_DIR"/*.pyc
    rm -rf "$PROJECT_DIR"/__pycache__
    rm -rf "$PROJECT_DIR"/utils/__pycache__
    rm -rf "$PROJECT_DIR"/core/__pycache__
    rm -rf "$PROJECT_DIR"/voice/__pycache__
    echo "Cleaned!"
}

# Diagnostics function
diagnose() {
    check_python
    setup_venv
    activate_venv
    echo "Running diagnostics..."
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
        background|bg)
            echo "Starting Purple AI in background mode..."
            setup_venv
            activate_venv
            cd "$PROJECT_DIR"
            nohup $PYTHON "$MAIN_SCRIPT" > logs/purple_ai.log 2>&1 &
            echo $! > "$PID_FILE"
            echo "Purple AI started in background (PID: $!)"
            echo "Log: logs/purple_ai.log"
            echo "Use './run.sh stop' to stop"
            exit 0
            ;;
        service)
            exec "$PROJECT_DIR/purple_service.sh" "${@:2}"
            exit 0
            ;;
        wake-words|wakewords)
            exec "$PROJECT_DIR/purple_service.sh" wake-words
            exit 0
            ;;
        --help|-h)
            echo "Purple AI - Voice-Controlled AI Assistant"
            echo ""
            echo "Usage: ./run.sh [option]"
            echo ""
            echo "Options:"
            echo "  (no args)    Run Purple AI (foreground)"
            echo "  background   Run in background (always listening)"
            echo "  stop         Stop running instance"
            echo "  clean        Clean temporary files"
            echo "  diagnose     Run system diagnostics"
            echo "  service      Background service control"
            echo "  wake-words   Show all active wake words"
            echo "  --help       Show this help"
            echo ""
            echo "Service commands:"
            echo "  ./run.sh service start      Start background service"
            echo "  ./run.sh service stop       Stop background service"
            echo "  ./run.sh service status     Show service status"
            echo "  ./run.sh service install    Auto-start on login"
            echo "  ./run.sh service logs       Watch live logs"
            echo ""
            echo "Always listening for wake words:"
            echo "  purple, hey purple, hello purple"
            echo "  ai, hey ai, computer, jarvis"
            echo "  wake up, listen, hello, hey"
            exit 0
            ;;
    esac
    
    # Kill any existing instances first
    kill_existing
    
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
