#!/bin/bash
# Purple AI Background Service
# Runs Purple AI always-on in background with auto-restart

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/data/purple_service.pid"
LOG_FILE="$SCRIPT_DIR/logs/service.log"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"
MAIN_SCRIPT="$SCRIPT_DIR/main.py"

# Create directories
mkdir -p "$SCRIPT_DIR/data"
mkdir -p "$SCRIPT_DIR/logs"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to check if service is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            return 0
        fi
    fi
    return 1
}

# Function to start the service
start_service() {
    if is_running; then
        echo -e "${YELLOW}Purple AI is already running (PID: $(cat $PID_FILE))${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Starting Purple AI Background Service...${NC}"
    
    # Start the Python script in background
    nohup "$VENV_PYTHON" "$MAIN_SCRIPT" >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    
    sleep 2
    
    if is_running; then
        echo -e "${GREEN}Purple AI started successfully! (PID: $(cat $PID_FILE))${NC}"
        echo -e "Log file: $LOG_FILE"
    else
        echo -e "${RED}Failed to start Purple AI${NC}"
        return 1
    fi
}

# Function to stop the service
stop_service() {
    if ! is_running; then
        echo -e "${YELLOW}Purple AI is not running${NC}"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    echo -e "${RED}Stopping Purple AI (PID: $PID)...${NC}"
    
    kill "$PID" 2>/dev/null
    sleep 2
    
    # Force kill if still running
    if kill -0 "$PID" 2>/dev/null; then
        kill -9 "$PID" 2>/dev/null
    fi
    
    rm -f "$PID_FILE"
    echo -e "${GREEN}Purple AI stopped${NC}"
}

# Function to restart the service
restart_service() {
    stop_service
    sleep 1
    start_service
}

# Function to show status
show_status() {
    echo -e "${GREEN}Purple AI Service Status${NC}"
    echo "========================"
    
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo -e "Status: ${GREEN}Running${NC} (PID: $PID)"
        echo "Log: $LOG_FILE"
        
        # Show memory usage
        ps -p "$PID" -o %cpu,%mem,etime 2>/dev/null | tail -1 | awk '{print "CPU: "$1"% | Memory: "$2"% | Uptime: "$3}'
    else
        echo -e "Status: ${RED}Stopped${NC}"
    fi
}

# Function to watch logs
watch_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo -e "${YELLOW}No log file found${NC}"
    fi
}

# Function to install as launch agent (auto-start on login)
install_autostart() {
    PLIST_FILE="$HOME/Library/LaunchAgents/com.purple.ai.plist"
    
    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.purple.ai</string>
    <key>ProgramArguments</key>
    <array>
        <string>$VENV_PYTHON</string>
        <string>$MAIN_SCRIPT</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LOG_FILE</string>
    <key>StandardErrorPath</key>
    <string>${LOG_FILE}.error</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:$SCRIPT_DIR/venv/bin</string>
    </dict>
</dict>
</plist>
EOF
    
    # Load the launch agent
    launchctl unload "$PLIST_FILE" 2>/dev/null
    launchctl load "$PLIST_FILE"
    
    echo -e "${GREEN}Auto-start installed!${NC}"
    echo -e "Purple AI will start automatically on login."
    echo -e "To uninstall: launchctl unload $PLIST_FILE"
}

# Function to uninstall auto-start
uninstall_autostart() {
    PLIST_FILE="$HOME/Library/LaunchAgents/com.purple.ai.plist"
    
    if [ -f "$PLIST_FILE" ]; then
        launchctl unload "$PLIST_FILE" 2>/dev/null
        rm -f "$PLIST_FILE"
        echo -e "${GREEN}Auto-start uninstalled${NC}"
    else
        echo -e "${YELLOW}Auto-start not installed${NC}"
    fi
}

# Function to show wake words
show_wake_words() {
    echo -e "${GREEN}Active Wake Words (Always Listening)${NC}"
    echo "======================================"
    echo ""
    echo "English:"
    echo "  - purple, hey purple, hello purple"
    echo "  - ok purple, okay purple, hi purple"
    echo "  - ai, hey ai, hello ai, hi ai"
    echo "  - computer, hey computer"
    echo "  - jarvis, alexa, siri"
    echo "  - wake up, listen, excuse me"
    echo "  - hello, hey, yo, morning"
    echo ""
    echo "Bangla:"
    echo "  - পার্পেল, হে পার্পেল"
    echo "  - কম্পিউটার, সহায়তা"
    echo "  - ওয়েক আপ, শোনো"
    echo "  - নমস্কার, হ্যালো"
    echo ""
    echo "Say any wake word followed by your command!"
}

# Main menu
case "${1:-}" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        show_status
        ;;
    logs)
        watch_logs
        ;;
    install)
        install_autostart
        ;;
    uninstall)
        uninstall_autostart
        ;;
    wake-words)
        show_wake_words
        ;;
    *)
        echo ""
        echo -e "${GREEN}Purple AI Background Service${NC}"
        echo "============================"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|install|uninstall|wake-words}"
        echo ""
        echo "Commands:"
        echo "  start       - Start Purple AI in background"
        echo "  stop        - Stop Purple AI"
        echo "  restart     - Restart Purple AI"
        echo "  status      - Show service status"
        echo "  logs        - Watch live logs"
        echo "  install     - Install auto-start on login"
        echo "  uninstall   - Remove auto-start"
        echo "  wake-words  - Show all active wake words"
        echo ""
        ;;
esac