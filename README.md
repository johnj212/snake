# Python Snake Game - Play Against the Computer

An enhanced Snake game implementation using Python and Pygame. Challenge yourself in single-player mode or test your skills against intelligent AI opponents in multiplayer mode!

## 🎮 Game Features

### Multiplayer Action
- **Player Snake**: Green snake controlled by you
- **AI Opponents**: 3 computer-controlled snakes (Blue, Yellow, Purple)
- **Competitive Gameplay**: All snakes compete for the same food
- **Smart AI**: Computer snakes actively seek food while avoiding collisions

### Enhanced Graphics & Performance
- **Optimized Window Size**: 500x500 pixels for better visibility
- **Smooth Animation**: 30 FPS screen refresh for fluid visuals
- **Balanced Speed**: Player moves at ~10 FPS, AI snakes at ~6 FPS
- **Visual Distinction**: Different colors for each snake with darker heads

## 📋 Requirements

- Python 3.x
- Pygame 2.5.2+

## 🚀 Installation

### Quick Install (Recommended)

1. Clone this repository:
```bash
git clone https://github.com/johnj212/snake.git
cd snake
```

2. Run the installation script for your platform:

**Windows:**
```cmd
install.bat
```

**macOS/Linux:**
```bash
./install.sh
```

The scripts will automatically:
- Check for Python 3.x installation
- Install pygame and dependencies
- Verify the installation
- Provide helpful error messages if needed

### Manual Installation

If you prefer manual installation:

```bash
# Make sure you have Python 3.x installed
python3 --version

# Install pygame
pip3 install pygame
# or
pip install -r requirements.txt
```

## 🕹️ How to Play

### Starting the Game

**Option 1: Direct launch**
```bash
python main.py
# or on some systems:
python3 main.py
```

**Option 2: Use the launcher script** (automatically detects Python version)
```bash
python run_game.py
```

### Game Modes

Choose from two exciting game modes:

#### 🟢 **1 - Single Player (Classic)**
- Traditional Snake gameplay
- Focus on growing as long as possible
- Avoid walls and your own tail
- Perfect for practicing and beating high scores

#### 🔵 **2 - Play Against Computer**
- Compete against 3 AI-controlled snakes
- All snakes fight for the same food
- Strategic gameplay with collision risks
- AI snakes respawn when eliminated

### Controls

- **Menu Navigation**: Press `1` for Single Player, `2` for AI Mode, `Q` to Quit
- **Arrow Keys**: Control your green snake's direction
- **ESC**: Return to main menu from any game mode
- **SPACE**: Restart game after game over
- **Objective**: Eat the red food to grow longer and increase your score

### Gameplay Mechanics

#### Single Player Mode
- Classic Snake rules: avoid walls and yourself
- Unlimited play until collision
- Score tracking for personal bests

#### Multiplayer Mode (vs Computer)
- **Multi-Snake Collisions**: Any snake hitting another snake dies
- **AI Respawn**: Dead AI snakes automatically respawn
- **Competitive Scoring**: Only the player earns points
- **Strategic Advantage**: Player moves faster than AI opponents

## ✨ Features

### Core Gameplay
- Score tracking and display
- Responsive controls with no input lag
- Grid-based movement system
- Real-time collision detection

### AI System
- Pathfinding AI that seeks food
- Collision avoidance algorithms
- Dynamic respawn system
- Balanced difficulty progression

### Visual & Technical
- Smooth 30 FPS display with controlled movement speed
- Color-coded snakes for easy identification
- Real-time AI snake counter
- Optimized rendering for performance

## 🎯 Game Strategy

- **Speed Advantage**: Use your faster movement to outmaneuver AI snakes
- **Positioning**: Control key areas around food spawns
- **Patience**: Let AI snakes eliminate each other
- **Growth**: Balance risk vs. reward when going for food

## 🛠️ Technical Details

- **Window Size**: 500x500 pixels (25×25 grid)
- **Frame Rate**: 30 FPS display, variable movement speeds
- **Player Speed**: 10 moves/second
- **AI Speed**: 6 moves/second
- **Grid Size**: 20×20 pixel cells
