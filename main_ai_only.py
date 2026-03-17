"""
Python Snake Game - AI Only Mode
A pygame-based implementation with a single AI-controlled snake
Watch the AI navigate and collect food autonomously
"""
import pygame
import random
import sys
from typing import List, Tuple, Optional

# Directional constants (must be defined before use)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game speed constants
FPS = 30  # Display refresh rate
AI_MOVE_DELAY = 5  # AI moves every 5 frames (~6 moves/sec)

# Grid constants
WINDOW_SIZE = 500  # Window size in pixels
GRID_SIZE = 20  # Size of each grid cell
GRID_COUNT = WINDOW_SIZE // GRID_SIZE  # Number of cells per dimension

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
CYAN = (0, 255, 255)
DARK_CYAN = (0, 200, 200)
GRAY = (128, 128, 128)

# Initialize Pygame with error handling
try:
    pygame.init()
except Exception as e:
    print(f"ERROR: Failed to initialize Pygame: {e}")
    sys.exit(1)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game - AI Only')
clock = pygame.time.Clock()

class Snake:
    """
    Base Snake class representing a snake entity in the game.
    Handles movement, collision detection, and rendering.
    """

    def __init__(self):
        """Initialize a new snake with default values."""
        self.reset()

    def get_head_position(self) -> Tuple[int, int]:
        """
        Get the current position of the snake's head.

        Returns:
            Tuple of (x, y) grid coordinates
        """
        return self.positions[0]

    def update(self) -> bool:
        """
        Update snake position (single snake mode without multi-snake collision).

        Returns:
            True if move was successful, False if collision occurred
        """
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)

        # Check for wall collision
        if (new[0] < 0 or new[0] >= GRID_COUNT or
            new[1] < 0 or new[1] >= GRID_COUNT):
            return False

        # Check for self collision (skip first 3 segments to allow tight turns)
        if new in self.positions[3:]:
            return False

        # Move snake
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        """Reset snake to initial state."""
        self.length = 1
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.color = GREEN

    def render(self, surface: pygame.Surface):
        """
        Render the snake on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        for i, p in enumerate(self.positions):
            color = DARK_GREEN if i == 0 else self.color
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

class AISnake(Snake):
    """
    AI-controlled snake with pathfinding and collision avoidance.
    Inherits from Snake and adds intelligent movement behavior.
    """

    def __init__(self, color: Tuple[int, int, int], dark_color: Tuple[int, int, int],
                 start_pos: Tuple[int, int]):
        """
        Initialize an AI snake with custom colors and starting position.

        Args:
            color: RGB tuple for snake body color
            dark_color: RGB tuple for snake head color
            start_pos: Starting (x, y) grid position
        """
        super().__init__()
        self.color = color
        self.dark_color = dark_color
        self.positions = [start_pos]

    def render(self, surface: pygame.Surface):
        """
        Render the AI snake with its custom colors.

        Args:
            surface: Pygame surface to draw on
        """
        for i, p in enumerate(self.positions):
            color = self.dark_color if i == 0 else self.color
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def ai_move(self, food_pos: Tuple[int, int]):
        """
        Calculate and execute AI movement toward food while avoiding collisions.
        Uses Manhattan distance heuristic to choose the best safe move.

        Args:
            food_pos: Target food position (x, y)
        """
        head = self.get_head_position()
        food_x, food_y = food_pos
        head_x, head_y = head

        # Calculate possible moves
        possible_moves = [UP, DOWN, LEFT, RIGHT]
        safe_moves = []

        for move in possible_moves:
            # Don't reverse direction (would cause instant self-collision)
            if move == (-self.direction[0], -self.direction[1]):
                continue

            new_x = head_x + move[0]
            new_y = head_y + move[1]

            # Check boundaries
            if new_x < 0 or new_x >= GRID_COUNT or new_y < 0 or new_y >= GRID_COUNT:
                continue

            # Check collision with self
            if (new_x, new_y) in self.positions[1:]:
                continue

            safe_moves.append(move)

        if not safe_moves:
            # No safe moves available, keep current direction
            return

        # Choose move that minimizes Manhattan distance to food
        best_move = safe_moves[0]
        best_distance = float('inf')

        for move in safe_moves:
            new_x = head_x + move[0]
            new_y = head_y + move[1]
            distance = abs(new_x - food_x) + abs(new_y - food_y)

            if distance < best_distance:
                best_distance = distance
                best_move = move

        self.direction = best_move

class Food:
    """
    Food item that snakes can eat to grow.
    Handles random spawning and rendering.
    """

    def __init__(self):
        """Initialize food with default position and color."""
        self.position = (0, 0)
        self.color = RED

    def randomize_position(self, snake: Optional[Snake] = None):
        """
        Randomize food position, avoiding occupied snake positions.

        Args:
            snake: Optional snake to avoid when spawning

        Note:
            If all positions are occupied (rare), falls back to random placement
        """
        if snake is None:
            self.position = (random.randint(0, GRID_COUNT-1),
                            random.randint(0, GRID_COUNT-1))
            return

        # Get all occupied positions
        occupied = set(snake.positions)

        # Find valid positions
        max_attempts = 100
        for _ in range(max_attempts):
            new_pos = (random.randint(0, GRID_COUNT-1),
                      random.randint(0, GRID_COUNT-1))
            if new_pos not in occupied:
                self.position = new_pos
                return

        # Fallback: if we can't find a free spot after max_attempts, place randomly
        self.position = (random.randint(0, GRID_COUNT-1),
                        random.randint(0, GRID_COUNT-1))

    def render(self, surface: pygame.Surface):
        """
        Render the food item on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        r = pygame.Rect((self.position[0] * GRID_SIZE,
                        self.position[1] * GRID_SIZE),
                       (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

def show_game_over(screen: pygame.Surface, score: int):
    """
    Display the game over screen with final score.

    Args:
        screen: Pygame surface to render on
        score: Final score to display
    """
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    game_over_text = font.render('AI Crashed!', True, WHITE)
    score_text = small_font.render(f'Final Score: {score}', True, WHITE)
    restart_text = small_font.render('Press SPACE to restart', True, GRAY)

    screen.blit(game_over_text,
                (WINDOW_SIZE//2 - game_over_text.get_width()//2,
                 WINDOW_SIZE//2 - 60))
    screen.blit(score_text,
                (WINDOW_SIZE//2 - score_text.get_width()//2,
                 WINDOW_SIZE//2))
    screen.blit(restart_text,
                (WINDOW_SIZE//2 - restart_text.get_width()//2,
                 WINDOW_SIZE//2 + 40))
    pygame.display.update()

def show_pause_screen(screen: pygame.Surface):
    """
    Display the pause screen overlay.

    Args:
        screen: Pygame surface to render on
    """
    # Create semi-transparent overlay
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    pause_text = font.render('PAUSED', True, WHITE)
    continue_text = small_font.render('Press P to continue', True, GRAY)

    screen.blit(pause_text,
                (WINDOW_SIZE//2 - pause_text.get_width()//2,
                 WINDOW_SIZE//2 - 40))
    screen.blit(continue_text,
                (WINDOW_SIZE//2 - continue_text.get_width()//2,
                 WINDOW_SIZE//2 + 20))
    pygame.display.update()

def ai_only_mode():
    """
    AI-only mode where you watch a single AI snake play the game.
    The AI navigates autonomously to collect food and grow.
    """
    # Initialize AI snake
    ai_snake = AISnake(CYAN, DARK_CYAN, (GRID_COUNT // 2, GRID_COUNT // 2))

    food = Food()
    food.randomize_position(ai_snake)
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    game_over = False
    paused = False
    ai_move_counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        # Reset AI snake
                        ai_snake = AISnake(CYAN, DARK_CYAN, (GRID_COUNT // 2, GRID_COUNT // 2))
                        food.randomize_position(ai_snake)
                        game_over = False
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                elif paused:
                    if event.key == pygame.K_p:
                        paused = False
                else:  # Game is running
                    if event.key == pygame.K_p:
                        paused = True
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        # Update game state
        if not game_over and not paused:
            ai_move_counter += 1

            if ai_move_counter >= AI_MOVE_DELAY:
                ai_move_counter = 0

                # AI decision making
                ai_snake.ai_move(food.position)

                # Update AI position
                if not ai_snake.update():
                    game_over = True
                    continue

                # Check food collision
                if ai_snake.get_head_position() == food.position:
                    ai_snake.length += 1
                    ai_snake.score += 1
                    food.randomize_position(ai_snake)

        # Draw everything
        screen.fill(BLACK)
        ai_snake.render(screen)
        food.render(screen)

        # Display stats
        score_text = font.render(f'Score: {ai_snake.score}', True, WHITE)
        length_text = small_font.render(f'Length: {ai_snake.length}', True, WHITE)
        mode_text = small_font.render('AI Only Mode - P:Pause ESC/Q:Quit', True, GRAY)
        watch_text = font.render('Watch the AI Play!', True, CYAN)

        screen.blit(score_text, (10, 10))
        screen.blit(length_text, (10, 45))
        screen.blit(watch_text, (WINDOW_SIZE//2 - watch_text.get_width()//2, 10))
        screen.blit(mode_text, (10, WINDOW_SIZE - 25))

        if game_over:
            show_game_over(screen, ai_snake.score)
        elif paused:
            show_pause_screen(screen)

        pygame.display.update()
        clock.tick(FPS)

def main():
    """
    Main entry point - directly starts AI-only mode.
    """
    ai_only_mode()

if __name__ == '__main__':
    main()
