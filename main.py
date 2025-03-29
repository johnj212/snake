import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
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
    snake = Snake()
    food = Food()
    font = pygame.font.Font(None, 36)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not game_over:
            # Update snake
            if not snake.update():
                game_over = True
                show_game_over(screen, snake.score)
                continue

            # Check if snake ate the food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()

            # Draw everything
            screen.fill(BLACK)
            snake.render(screen)
            food.render(screen)
            
            # Draw score
            score_text = font.render(f'Score: {snake.score}', True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.update()
            clock.tick(10)  # Control game speed

if __name__ == '__main__':
    main() 