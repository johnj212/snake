# Python Snake Game - Multiplayer Edition

An enhanced Snake game implementation using Python and Pygame, featuring AI-controlled opponents and smooth gameplay.

## 🎮 Game Features

### Multiplayer Action
- **Player Snake**: Green snake controlled by you
- **AI Opponents**: 3 computer-controlled snakes (Blue, Yellow, Purple)
- **Competitive Gameplay**: All snakes compete for the same food
- **Smart AI**: Computer snakes actively seek food while avoiding collisions

### Enhanced Graphics & Performance
- **Optimized Window Size**: 500x500 pixels for better visibility
- **Smooth Animation**: 30 FPS screen refresh for fluid visuals
- **Balanced Speed**: Player moves at ~10 FPS, AI snakes at ~7.5 FPS
- **Visual Distinction**: Different colors for each snake with darker heads

## 📋 Requirements

- Python 3.x
- Pygame 2.5.2+

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/johnj212/snake.git
cd snake
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 🕹️ How to Play

Run the game:
```bash
python main.py
```

### Controls

- **Arrow Keys**: Control your green snake's direction
- **Objective**: Eat the red food to grow longer and increase your score
- **Avoid**: Hitting walls, yourself, or other snakes
- **Game Over**: Press **SPACE** to restart when you die

### Gameplay Mechanics

- **Multi-Snake Collisions**: Any snake hitting another snake dies
- **AI Respawn**: Dead AI snakes automatically respawn
- **Competitive Scoring**: Only the player earns points
- **Strategic Advantage**: Player moves slightly faster than AI opponents

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
- **AI Speed**: 7.5 moves/second
- **Grid Size**: 20×20 pixel cells
