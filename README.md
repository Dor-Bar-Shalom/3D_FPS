# GrandMaizer

GrandMaizer is a single-player FPS game built in Python using Pygame. The game features custom AI, raycasting rendering, multiple enemy types, and dynamic map-based gameplay.

## 🎯 Game Overview

You play as a space warrior trying to survive on a hostile alien planet. Your mission: eliminate all enemies on the map and be the last one standing.

- Choose from **two maps**
- Select **two difficulty levels** (10 or 20 enemies)
- Encounter 3 types of enemies: ranged, melee, and boss
- Use your weapon with precision and timing
- Regenerate health between fights
- Game ends when you either survive or fall

## 🧠 Technologies

- **Python 3.x**
- **Pygame** – rendering, game loop, input, sound
- **Tkinter** – for pre-game GUI (map and difficulty selection)
- **Raycasting** – for pseudo-3D visual experience
- **Custom AI** – pathfinding using BFS, enemy line-of-sight logic

## 📁 Project Structure

- `main.py`: Game runner and loop
- `opening_screen.py`: Tkinter-based menu for setup
- `player.py`, `npc.py`: Game entities and behavior
- `entityManager.py`: Manages all NPCs and game logic
- `renderingEngine.py`: Visual rendering and UI effects
- `raycasting.py`: Wall and object projection logic
- `map.py`, `graphNavigator.py`: Map data and AI pathfinding
- `sound.py`, `weapon.py`: Audio and shooting mechanics
- `spriteEntity.py`: Base sprite and animation classes

## 🕹 How to Run

1. Install Python 3.x
2. Install dependencies:
   ```bash
   pip install pygame
