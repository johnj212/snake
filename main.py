import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 500  # Increased by 25% (400 * 1.25 = 500)
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

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

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.reset()

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)
        
        # Check for wall collision
        if (new[0] < 0 or new[0] >= GRID_COUNT or 
            new[1] < 0 or new[1] >= GRID_COUNT):
            return False
            
        # Check for self collision
        if new in self.positions[3:]:
            return False
            
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
        
    def update_with_collision_check(self, all_snakes):
        """Update snake position with collision checking against other snakes"""
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)
        
        # Check for wall collision
        if (new[0] < 0 or new[0] >= GRID_COUNT or 
            new[1] < 0 or new[1] >= GRID_COUNT):
            return False
            
        # Check for self collision
        if new in self.positions[3:]:
            return False
            
        # Check for collision with other snakes
        for other_snake in all_snakes:
            if other_snake != self and new in other_snake.positions:
                return False
                
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.color = GREEN

    def render(self, surface):
        for i, p in enumerate(self.positions):
            color = DARK_GREEN if i == 0 else self.color
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

class ComputerSnake(Snake):
    def __init__(self, color, dark_color, start_pos):
        super().__init__()
        self.color = color
        self.dark_color = dark_color
        self.positions = [start_pos]
        self.ai_target = None

    def render(self, surface):
        for i, p in enumerate(self.positions):
            color = self.dark_color if i == 0 else self.color
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def ai_move(self, food_pos, all_snakes):
        """Simple AI that moves toward food while avoiding collisions"""
        head = self.get_head_position()
        food_x, food_y = food_pos
        head_x, head_y = head
        
        # Get all occupied positions from all snakes
        occupied_positions = set()
        for snake in all_snakes:
            if snake != self:
                occupied_positions.update(snake.positions)
        
        # Calculate possible moves
        possible_moves = [UP, DOWN, LEFT, RIGHT]
        safe_moves = []
        
        for move in possible_moves:
            # Don't reverse direction
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
            # No safe moves, keep current direction
            return
            
        # Choose move that gets closer to food
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

    def update_with_collision_check(self, all_snakes):
        """Update snake position with collision checking against other snakes"""
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)
        
        # Check for wall collision
        if (new[0] < 0 or new[0] >= GRID_COUNT or 
            new[1] < 0 or new[1] >= GRID_COUNT):
            return False
            
        # Check for self collision
        if new in self.positions[3:]:
            return False
            
        # Check for collision with other snakes
        for other_snake in all_snakes:
            if other_snake != self and new in other_snake.positions:
                return False
                
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_COUNT-1),
                        random.randint(0, GRID_COUNT-1))

    def render(self, surface):
        r = pygame.Rect((self.position[0] * GRID_SIZE,
                        self.position[1] * GRID_SIZE),
                       (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def show_game_over(screen, score):
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

def main():
    # Create player snake
    player_snake = Snake()
    
    # Create AI snakes with different colors and positions
    ai_snakes = [
        ComputerSnake(BLUE, DARK_BLUE, (5, 5)),
        ComputerSnake(YELLOW, DARK_YELLOW, (GRID_COUNT-5, 5)),
        ComputerSnake(PURPLE, DARK_PURPLE, (5, GRID_COUNT-5))
    ]
    
    # All snakes for collision detection
    all_snakes = [player_snake] + ai_snakes
    
    food = Food()
    font = pygame.font.Font(None, 24)  # Smaller font for smaller window
    game_over = False
    move_counter = 0
    ai_move_counter = 0
    move_delay = 3  # Player snake moves every 3 frames (10 FPS movement at 30 FPS screen)
    ai_move_delay = 4  # AI snakes move every 4 frames (~7.5 FPS, 25% slower than player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    # Reset all snakes
                    player_snake.reset()
                    for ai_snake in ai_snakes:
                        ai_snake.reset()
                    food.randomize_position()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and player_snake.direction != DOWN:
                        player_snake.direction = UP
                    elif event.key == pygame.K_DOWN and player_snake.direction != UP:
                        player_snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and player_snake.direction != RIGHT:
                        player_snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and player_snake.direction != LEFT:
                        player_snake.direction = RIGHT

        if not game_over:
            # Increment move counters
            move_counter += 1
            ai_move_counter += 1
            
            # Update player snake when its counter reaches delay
            player_should_move = move_counter >= move_delay
            if player_should_move:
                move_counter = 0  # Reset player counter
                
                # Update player snake
                if not player_snake.update_with_collision_check(all_snakes):
                    game_over = True
                    show_game_over(screen, player_snake.score)
                    continue
            
            # Update AI snakes when their counter reaches delay
            ai_should_move = ai_move_counter >= ai_move_delay
            if ai_should_move:
                ai_move_counter = 0  # Reset AI counter
                
                # Update AI snake directions
                for ai_snake in ai_snakes:
                    ai_snake.ai_move(food.position, all_snakes)
                
                # Update AI snake positions
                snakes_to_remove = []
                for ai_snake in ai_snakes:
                    if not ai_snake.update_with_collision_check(all_snakes):
                        snakes_to_remove.append(ai_snake)
                
                # Remove dead AI snakes
                for dead_snake in snakes_to_remove:
                    ai_snakes.remove(dead_snake)
                    all_snakes.remove(dead_snake)
                
                # Respawn AI snakes if they all died
                if len(ai_snakes) == 0:
                    ai_snakes = [
                        ComputerSnake(BLUE, DARK_BLUE, (5, 5)),
                        ComputerSnake(YELLOW, DARK_YELLOW, (GRID_COUNT-5, 5)),
                        ComputerSnake(PURPLE, DARK_PURPLE, (5, GRID_COUNT-5))
                    ]
                    all_snakes = [player_snake] + ai_snakes

            # Check if any snake ate the food (check after any movement)
            if player_should_move or ai_should_move:
                for snake in all_snakes:
                    if snake.get_head_position() == food.position:
                        snake.length += 1
                        if snake == player_snake:
                            snake.score += 1
                        food.randomize_position()
                        break

            # Draw everything
            screen.fill(BLACK)
            
            # Render all snakes
            for snake in all_snakes:
                snake.render(screen)
            
            food.render(screen)
            
            # Draw score and snake count
            score_text = font.render(f'Score: {player_snake.score}', True, WHITE)
            snakes_text = font.render(f'AI Snakes: {len(ai_snakes)}', True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(snakes_text, (10, 30))

            pygame.display.update()
            clock.tick(30)  # Control game speed

if __name__ == '__main__':
    main() 