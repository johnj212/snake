#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}   Python Snake Game - Installation Script${NC}"
echo -e "${BLUE}        Play Against the Computer!${NC}"
echo -e "${BLUE}===============================================${NC}"
echo

# Check if Python 3 is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | grep -o 'Python 3')
    if [[ -n "$PYTHON_VERSION" ]]; then
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        echo -e "${RED}ERROR: Python 3 is required but not found${NC}"
        echo
        echo "Please install Python 3.x:"
        echo "  macOS: brew install python3 (or download from https://python.org)"
        echo "  Linux: sudo apt install python3 python3-pip (Ubuntu/Debian)"
        echo "         sudo yum install python3 python3-pip (RHEL/CentOS)"
        echo
        exit 1
    fi
else
    echo -e "${RED}ERROR: Python is not installed${NC}"
    echo
    echo "Please install Python 3.x:"
    echo "  macOS: brew install python3 (or download from https://python.org)"
    echo "  Linux: sudo apt install python3 python3-pip (Ubuntu/Debian)"
    echo "         sudo yum install python3 python3-pip (RHEL/CentOS)"
    echo
    exit 1
fi

echo -e "${GREEN}Python detected:${NC}"
$PYTHON_CMD --version
echo

# Check if pip is available
if ! command -v $PIP_CMD &> /dev/null; then
    echo -e "${RED}ERROR: pip is not available${NC}"
    echo "Please install pip:"
    echo "  macOS: python3 -m ensurepip --upgrade"
    echo "  Linux: sudo apt install python3-pip (Ubuntu/Debian)"
    echo
    exit 1
fi

echo -e "${YELLOW}Installing required packages...${NC}"
echo

# Install pygame
echo -e "${YELLOW}Installing pygame...${NC}"
if $PIP_CMD install pygame==2.5.2; then
    echo -e "${GREEN}pygame installed successfully!${NC}"
else
    echo -e "${YELLOW}WARNING: Failed to install specific pygame version, trying latest...${NC}"
    if $PIP_CMD install pygame; then
        echo -e "${GREEN}pygame installed successfully!${NC}"
    else
        echo -e "${RED}ERROR: Failed to install pygame${NC}"
        echo "Please check your internet connection and try again"
        echo "You may also need to install system dependencies:"
        echo "  macOS: Make sure Xcode command line tools are installed"
        echo "  Linux: sudo apt install python3-dev libsdl2-dev (Ubuntu/Debian)"
        echo
        exit 1
    fi
fi

echo
echo -e "${GREEN}===============================================${NC}"
echo -e "${GREEN}          Installation Complete!${NC}"
echo -e "${GREEN}===============================================${NC}"
echo
echo -e "${BLUE}The Snake game is now ready to play!${NC}"
echo
echo -e "${YELLOW}To start the game, run:${NC}"
echo -e "  ${GREEN}$PYTHON_CMD main.py${NC}"
echo
echo -e "${YELLOW}Game Features:${NC}"
echo "  - Single Player: Classic Snake gameplay"
echo "  - AI Mode: Play against 3 computer opponents"
echo "  - Balanced gameplay with strategic advantages"
echo
echo -e "${YELLOW}Controls:${NC}"
echo "  - Menu: Press 1 for Single Player, 2 for AI Mode"
echo "  - Game: Use arrow keys to control your snake"
echo "  - ESC: Return to menu anytime"
echo
echo -e "${BLUE}Have fun playing Snake!${NC}"
echo
