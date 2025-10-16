#!/bin/bash
#
# Roblox Keeper Launcher
# Handles starting, stopping, and status checking
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
KEEPER_SCRIPT="$SCRIPT_DIR/scripts/keeper.py"
LOG_DIR="$SCRIPT_DIR/logs"
SCREENSHOT_DIR="$SCRIPT_DIR/screenshots"
PID_FILE="$LOG_DIR/keeper.pid"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                    🎮 ROBLOX KEEPER LAUNCHER                     ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo ""
}

check_dependencies() {
    echo "Checking dependencies..."

    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is not installed${NC}"
        exit 1
    fi

    if ! python3 -c "import pyautogui" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  pyautogui not installed. Installing...${NC}"
        pip3 install pyautogui
    fi

    echo -e "${GREEN}✓ All dependencies met${NC}"
}

is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0
        fi
    fi
    return 1
}

start_keeper() {
    if is_running; then
        echo -e "${YELLOW}⚠️  Keeper is already running!${NC}"
        echo "Run './launch.sh status' to check status"
        exit 0
    fi

    echo "Starting Roblox Keeper..."

    # Check if Roblox is running
    if ! pgrep -i roblox > /dev/null; then
        echo -e "${RED}❌ Roblox is not running!${NC}"
        echo "Please start Roblox first, then run this script again."
        exit 1
    fi

    # Start keeper in background
    nohup python3 "$KEEPER_SCRIPT" > "$LOG_DIR/output.log" 2>&1 &
    PID=$!
    echo $PID > "$PID_FILE"

    sleep 2

    if is_running; then
        echo -e "${GREEN}✓ Keeper started successfully!${NC}"
        echo "  PID: $PID"
        echo "  Logs: $LOG_DIR/keeper.log"
        echo "  Status: $LOG_DIR/status.json"
        echo ""
        echo "Run './launch.sh status' to check status"
        echo "Run './launch.sh stop' to stop"
    else
        echo -e "${RED}❌ Failed to start keeper${NC}"
        cat "$LOG_DIR/output.log"
        exit 1
    fi
}

stop_keeper() {
    if ! is_running; then
        echo -e "${YELLOW}⚠️  Keeper is not running${NC}"
        exit 0
    fi

    PID=$(cat "$PID_FILE")
    echo "Stopping Roblox Keeper (PID: $PID)..."

    kill $PID
    rm -f "$PID_FILE"

    echo -e "${GREEN}✓ Keeper stopped${NC}"
}

show_status() {
    if ! is_running; then
        echo -e "${RED}❌ Keeper is not running${NC}"
        echo "Run './launch.sh start' to start"
        exit 0
    fi

    PID=$(cat "$PID_FILE")
    echo -e "${GREEN}✓ Keeper is running (PID: $PID)${NC}"
    echo ""

    if [ -f "$SCRIPT_DIR/scripts/view_status.py" ]; then
        python3 "$SCRIPT_DIR/scripts/view_status.py"
    fi
}

show_logs() {
    if [ -f "$LOG_DIR/keeper.log" ]; then
        echo "Latest logs:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        tail -20 "$LOG_DIR/keeper.log"
    else
        echo "No logs found"
    fi
}

show_help() {
    echo "Usage: ./launch.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start    - Start the keeper"
    echo "  stop     - Stop the keeper"
    echo "  restart  - Restart the keeper"
    echo "  status   - Show current status"
    echo "  logs     - Show recent logs"
    echo "  help     - Show this help"
    echo ""
}

# Main
print_header
check_dependencies

case "${1:-}" in
    start)
        start_keeper
        ;;
    stop)
        stop_keeper
        ;;
    restart)
        stop_keeper
        sleep 1
        start_keeper
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
