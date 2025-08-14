#!/usr/bin/env python3
"""
Screenshot helper script for Snake Game documentation
This script provides instructions for taking screenshots of the game
"""

import os
import sys

def create_placeholder_instructions():
    """Create instruction file for taking screenshots"""
    
    instructions = """
# Snake Game Screenshot Instructions

To create professional screenshots for the README, follow these steps:

## 📸 Screenshots Needed:

1. **menu.png** - Main menu screen
   - Run: python main.py
   - Take screenshot of the menu with "Choose Game Mode" options
   - Save as: screenshots/menu.png

2. **single_player.png** - Single player gameplay
   - Select option "1" for Single Player
   - Play until snake has grown (eat a few food items)
   - Take screenshot showing snake, food, and score
   - Save as: screenshots/single_player.png

3. **multiplayer.png** - AI multiplayer mode
   - Select option "2" for AI Mode
   - Play until AI snakes are visible and active
   - Take screenshot showing multiple colored snakes competing
   - Save as: screenshots/multiplayer.png

## 🖥️ Screenshot Tips:

### macOS:
- Cmd+Shift+4: Select area to screenshot
- Cmd+Shift+3: Full screen screenshot

### Windows:
- Snipping Tool or Snip & Sketch
- Print Screen + Paint

### Linux:
- gnome-screenshot -a (area selection)
- scrot -s (area selection)

## 📐 Recommended Settings:

- Focus on the game window only
- Ensure good visibility of all elements
- Capture during active gameplay for dynamic shots
- Make sure text is readable

## 🎮 Gameplay Scenarios:

### Menu Screenshot:
- Clean main menu with all options visible
- Good contrast and readable text

### Single Player Screenshot:
- Snake with length 5-10 segments
- Food visible on screen
- Score showing progress
- Clean game area

### Multiplayer Screenshot:
- Player snake (green) visible
- At least 2-3 AI snakes (blue, yellow, purple)
- Food item on screen
- AI snake counter showing
- Active gameplay moment

After taking screenshots, the README will automatically display them!
"""

    with open('screenshots/README_INSTRUCTIONS.txt', 'w') as f:
        f.write(instructions.strip())
    
    print("📸 Screenshot instructions created!")
    print("📁 Check screenshots/README_INSTRUCTIONS.txt for detailed guidance")

def main():
    # Create screenshots directory if it doesn't exist
    os.makedirs('screenshots', exist_ok=True)
    
    # Create instruction file
    create_placeholder_instructions()
    
    print("\n" + "="*60)
    print("  SNAKE GAME SCREENSHOT HELPER")
    print("="*60)
    print()
    print("This script helps you document the Snake game with screenshots.")
    print()
    print("📋 TODO: Take these 3 screenshots:")
    print("   1. screenshots/menu.png - Main menu")
    print("   2. screenshots/single_player.png - Single player mode")  
    print("   3. screenshots/multiplayer.png - AI multiplayer mode")
    print()
    print("📖 Detailed instructions: screenshots/README_INSTRUCTIONS.txt")
    print()
    print("🎮 To start the game for screenshots:")
    print("   python main.py")
    print()
    print("✨ Once you add the screenshots, they'll appear in the README!")
    print("="*60)

if __name__ == "__main__":
    main()
