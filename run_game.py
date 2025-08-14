#!/usr/bin/env python3
"""
Simple launcher script for the Snake game that handles Python version detection
"""
import sys
import subprocess
import os

def find_python():
    """Find the appropriate Python executable"""
    python_commands = ['python3', 'python']
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, check=True)
            if 'Python 3' in result.stdout:
                return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    return None

def main():
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("ERROR: main.py not found!")
        print("Please run this script from the Snake game directory.")
        sys.exit(1)
    
    # Find Python
    python_cmd = find_python()
    if not python_cmd:
        print("ERROR: Python 3 is required but not found!")
        print("\nPlease install Python 3.x:")
        if sys.platform == "darwin":  # macOS
            print("  macOS: Download from https://python.org or use 'brew install python3'")
        elif sys.platform.startswith("linux"):  # Linux
            print("  Linux: sudo apt install python3 (Ubuntu/Debian)")
            print("         sudo yum install python3 (RHEL/CentOS)")
        elif sys.platform.startswith("win"):  # Windows
            print("  Windows: Download from https://python.org")
            print("           Make sure to check 'Add Python to PATH' during installation")
        sys.exit(1)
    
    print(f"🐍 Starting Snake Game with {python_cmd}...")
    print("🎮 Choose your game mode and have fun!")
    print()
    
    try:
        # Run the game
        subprocess.run([python_cmd, 'main.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Game failed to start (exit code: {e.returncode})")
        print("Make sure pygame is installed by running the install script first.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Thanks for playing Snake!")
        sys.exit(0)

if __name__ == "__main__":
    main()
