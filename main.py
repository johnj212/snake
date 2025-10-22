"""
Python Snake Game with Single Player and AI Multiplayer Modes
A pygame-based implementation with intelligent AI opponents
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
PLAYER_MOVE_DELAY = 3  # Player moves every 3 frames (~10 moves/sec)
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
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
PURPLE = (255, 0, 255)
DARK_PURPLE = (200, 0, 200)
GRAY = (128, 128, 128)

# Initialize Pygame with error handling
try:
    pygame.init()
except Exception as e:
    print(f"ERROR: Failed to initialize Pygame: {e}")
    sys.exit(1)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
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
        Update snake position (single player mode without multi-snake collision).

        Returns:
            True if move was successful, False if collision occurred
        """
        return self.update_with_collision_check([])

    def update_with_collision_check(self, all_snakes: List['Snake']) -> bool:
        """
        Update snake position with full collision checking.
        Checks for wall collisions, self-collisions, and collisions with other snakes.

        Args:
            all_snakes: List of all snakes to check for collisions

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

        # Check for collision with other snakes
        for other_snake in all_snakes:
            if other_snake != self and new in other_snake.positions:
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

class ComputerSnake(Snake):
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

    def ai_move(self, food_pos: Tuple[int, int], all_snakes: List['Snake']):
        """
        Calculate and execute AI movement toward food while avoiding collisions.
        Uses Manhattan distance heuristic to choose the best safe move.

        Args:
            food_pos: Target food position (x, y)
            all_snakes: List of all snakes to avoid
        """
        head = self.get_head_position()
        food_x, food_y = food_pos
        head_x, head_y = head

        # Get all occupied positions from all snakes (excluding self)
        occupied_positions = set()
        for snake in all_snakes:
            if snake != self:
                occupied_positions.update(snake.positions)

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

            # Check collision with other snakes and self
            if (new_x, new_y) in occupied_positions or (new_x, new_y) in self.positions[1:]:
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

    def randomize_position(self, snakes: Optional[List[Snake]] = None):
        """
        Randomize food position, avoiding occupied snake positions.

        Args:
            snakes: Optional list of snakes to avoid when spawning

        Note:
            If all positions are occupied (rare), falls back to random placement
        """
        if snakes is None:
            snakes = []

        # Get all occupied positions
        occupied = set()
        for snake in snakes:
            occupied.update(snake.positions)

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

def show_menu(screen: pygame.Surface):
    """
    Display the game mode selection menu.

    Args:
        screen: Pygame surface to render the menu on
    """
    font = pygame.font.Font(None, 74)
    medium_font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)

    title_text = font.render('Snake Game', True, WHITE)
    subtitle_text = medium_font.render('Choose Game Mode', True, WHITE)
    single_text = small_font.render('1 - Single Player (Classic)', True, GREEN)
    ai_text = small_font.render('2 - Play Against Computer', True, BLUE)
    quit_text = small_font.render('Q - Quit', True, GRAY)

    # Center the text
    screen.fill(BLACK)
    screen.blit(title_text,
                (WINDOW_SIZE//2 - title_text.get_width()//2, 100))
    screen.blit(subtitle_text,
                (WINDOW_SIZE//2 - subtitle_text.get_width()//2, 180))
    screen.blit(single_text,
                (WINDOW_SIZE//2 - single_text.get_width()//2, 250))
    screen.blit(ai_text,
                (WINDOW_SIZE//2 - ai_text.get_width()//2, 290))
    screen.blit(quit_text,
                (WINDOW_SIZE//2 - quit_text.get_width()//2, 350))

    pygame.display.update()

def show_game_over(screen: pygame.Surface, score: int):
    """
    Display the game over screen with final score.

    Args:
        screen: Pygame surface to render on
        score: Final score to display
    """
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    game_over_text = font.render('Game Over!', True, WHITE)
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

def single_player_mode():
    """
    Classic single player Snake game mode.
    Control a snake to eat food and grow as long as possible.
    """
    player_snake = Snake()
    food = Food()
    food.randomize_position([player_snake])
    font = pygame.font.Font(None, 36)
    game_over = False
    paused = False
    move_counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        player_snake.reset()
                        food.randomize_position([player_snake])
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        return  # Return to menu
                elif paused:
                    if event.key == pygame.K_p:
                        paused = False
                else:  # Game is running
                    if event.key == pygame.K_UP and player_snake.direction != DOWN:
                        player_snake.direction = UP
                    elif event.key == pygame.K_DOWN and player_snake.direction != UP:
                        player_snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and player_snake.direction != RIGHT:
                        player_snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and player_snake.direction != LEFT:
                        player_snake.direction = RIGHT
                    elif event.key == pygame.K_p:
                        paused = True
                    elif event.key == pygame.K_ESCAPE:
                        return  # Return to menu

        # Update game state
        if not game_over and not paused:
            move_counter += 1
            if move_counter >= PLAYER_MOVE_DELAY:
                move_counter = 0

                if not player_snake.update():
                    game_over = True
                    continue

                # Check food collision
                if player_snake.get_head_position() == food.position:
                    player_snake.length += 1
                    player_snake.score += 1
                    food.randomize_position([player_snake])

        # Draw everything
        screen.fill(BLACK)
        player_snake.render(screen)
        food.render(screen)

        score_text = font.render(f'Score: {player_snake.score}', True, WHITE)
        mode_text = font.render('Single Player - P:Pause ESC:Menu', True, GRAY)
        screen.blit(score_text, (10, 10))
        screen.blit(mode_text, (10, WINDOW_SIZE - 25))

        if game_over:
            show_game_over(screen, player_snake.score)
        elif paused:
            show_pause_screen(screen)

        pygame.display.update()
        clock.tick(FPS)

def ai_mode():
    """
    Multiplayer mode with AI opponents.
    Compete against 3 computer-controlled snakes for food.
    """
    # Initialize snakes
    player_snake = Snake()
    ai_snakes = [
        ComputerSnake(BLUE, DARK_BLUE, (5, 5)),
        ComputerSnake(YELLOW, DARK_YELLOW, (GRID_COUNT-6, 5)),
        ComputerSnake(PURPLE, DARK_PURPLE, (5, GRID_COUNT-6))
    ]
    all_snakes = [player_snake] + ai_snakes

    food = Food()
    food.randomize_position(all_snakes)
    font = pygame.font.Font(None, 24)
    game_over = False
    paused = False
    move_counter = 0
    ai_move_counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        # Reset all snakes
                        player_snake.reset()
                        ai_snakes = [
                            ComputerSnake(BLUE, DARK_BLUE, (5, 5)),
                            ComputerSnake(YELLOW, DARK_YELLOW, (GRID_COUNT-6, 5)),
                            ComputerSnake(PURPLE, DARK_PURPLE, (5, GRID_COUNT-6))
                        ]
                        all_snakes = [player_snake] + ai_snakes
                        food.randomize_position(all_snakes)
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        return  # Return to menu
                elif paused:
                    if event.key == pygame.K_p:
                        paused = False
                else:  # Game is running
                    if event.key == pygame.K_UP and player_snake.direction != DOWN:
                        player_snake.direction = UP
                    elif event.key == pygame.K_DOWN and player_snake.direction != UP:
                        player_snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and player_snake.direction != RIGHT:
                        player_snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and player_snake.direction != LEFT:
                        player_snake.direction = RIGHT
                    elif event.key == pygame.K_p:
                        paused = True
                    elif event.key == pygame.K_ESCAPE:
                        return  # Return to menu

        # Update game state
        if not game_over and not paused:
            move_counter += 1
            ai_move_counter += 1

            player_should_move = move_counter >= PLAYER_MOVE_DELAY
            if player_should_move:
                move_counter = 0
                if not player_snake.update_with_collision_check(all_snakes):
                    game_over = True
                    continue

            ai_should_move = ai_move_counter >= AI_MOVE_DELAY
            if ai_should_move:
                ai_move_counter = 0

                # AI decision making
                for ai_snake in ai_snakes:
                    ai_snake.ai_move(food.position, all_snakes)

                # Update AI positions and remove dead snakes
                snakes_to_remove = []
                for ai_snake in ai_snakes:
                    if not ai_snake.update_with_collision_check(all_snakes):
                        snakes_to_remove.append(ai_snake)

                for dead_snake in snakes_to_remove:
                    ai_snakes.remove(dead_snake)
                    all_snakes.remove(dead_snake)

                # Respawn AI snakes if all died
                if len(ai_snakes) == 0:
                    ai_snakes = [
                        ComputerSnake(BLUE, DARK_BLUE, (5, 5)),
                        ComputerSnake(YELLOW, DARK_YELLOW, (GRID_COUNT-6, 5)),
                        ComputerSnake(PURPLE, DARK_PURPLE, (5, GRID_COUNT-6))
                    ]
                    all_snakes = [player_snake] + ai_snakes

            # Check food collision (only when snakes have moved)
            if player_should_move or ai_should_move:
                for snake in all_snakes:
                    if snake.get_head_position() == food.position:
                        snake.length += 1
                        if snake == player_snake:
                            snake.score += 1
                        food.randomize_position(all_snakes)
                        break

        # Draw everything
        screen.fill(BLACK)
        for snake in all_snakes:
            snake.render(screen)
        food.render(screen)

        score_text = font.render(f'Score: {player_snake.score}', True, WHITE)
        snakes_text = font.render(f'AI Snakes: {len(ai_snakes)}', True, WHITE)
        mode_text = font.render('VS Computer - P:Pause ESC:Menu', True, GRAY)
        screen.blit(score_text, (10, 10))
        screen.blit(snakes_text, (10, 30))
        screen.blit(mode_text, (10, WINDOW_SIZE - 25))

        if game_over:
            show_game_over(screen, player_snake.score)
        elif paused:
            show_pause_screen(screen)

        pygame.display.update()
        clock.tick(FPS)

def main():
    """
    Main menu loop and game mode selection.
    Displays menu and handles user input for mode selection.
    """
    while True:
        show_menu(screen)

        # Process all events (not just one per frame)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    single_player_mode()
                elif event.key == pygame.K_2:
                    ai_mode()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)

if __name__ == '__main__':
    main() 