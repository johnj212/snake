"""
Tron-Style Neon Snake — standalone variant of the Snake game.
All visuals rendered procedurally with pygame (no external assets).
"""
import pygame
import pygame.freetype
import random
import sys
import math
from collections import deque

# ── Constants ──────────────────────────────────────────────────────────────────
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

FPS              = 30
PLAYER_MOVE_DELAY = 3   # frames between player moves (~10/s)
AI_MOVE_DELAY    = 5    # frames between AI moves (~6/s)

WINDOW_SIZE = 500
GRID_SIZE   = 20
GRID_COUNT  = WINDOW_SIZE // GRID_SIZE

# ── Neon Palette ───────────────────────────────────────────────────────────────
NEON_BG       = (5,   5,   15)
PLAYER_NEON   = (0,   229, 255)
PLAYER_HEAD   = (180, 255, 255)
AI1_NEON      = (255, 0,   200)
AI1_HEAD      = (255, 140, 230)
AI2_NEON      = (255, 100,  0)
AI2_HEAD      = (255, 200, 100)
FOOD_CORE     = (255, 255, 200)
UI_GAMEOVER   = (255, 30,   80)
GRID_LINE_COL = (0,   80,  120)

TRAIL_LENGTH  = 15
TRAIL_START_ALPHA = 160
TRAIL_FADE_PER_FRAME = 6

GLOW_LAYERS   = 4
BORDER_RADIUS = 5

# ── Logic classes (no rendering) ───────────────────────────────────────────────

class SnakeLogic:
    def __init__(self):
        self.reset()

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length    = 1
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score     = 0

    def update(self):
        return self._move([])

    def update_with_collision_check(self, all_snakes):
        return self._move(all_snakes)

    def _move(self, all_snakes):
        cur = self.get_head_position()
        nx = cur[0] + self.direction[0]
        ny = cur[1] + self.direction[1]
        new = (nx, ny)

        if nx < 0 or nx >= GRID_COUNT or ny < 0 or ny >= GRID_COUNT:
            return False
        if new in self.positions[3:]:
            return False
        for other in all_snakes:
            if other is not self and new in other.positions:
                return False

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True


class ComputerSnakeLogic(SnakeLogic):
    def __init__(self, start_pos):
        super().__init__()
        self.positions = [start_pos]

    def ai_move(self, food_pos, all_snakes):
        head_x, head_y = self.get_head_position()
        food_x, food_y = food_pos

        occupied = set()
        for s in all_snakes:
            if s is not self:
                occupied.update(s.positions)

        candidates = []
        for move in [UP, DOWN, LEFT, RIGHT]:
            if move == (-self.direction[0], -self.direction[1]):
                continue
            nx, ny = head_x + move[0], head_y + move[1]
            if nx < 0 or nx >= GRID_COUNT or ny < 0 or ny >= GRID_COUNT:
                continue
            if (nx, ny) in occupied or (nx, ny) in self.positions[1:]:
                continue
            candidates.append(move)

        if not candidates:
            return

        best = min(candidates, key=lambda m: (
            abs(head_x + m[0] - food_x) + abs(head_y + m[1] - food_y)
        ))
        self.direction = best


class FoodLogic:
    def __init__(self):
        self.position = (0, 0)

    def randomize_position(self, snakes):
        occupied = set()
        for s in snakes:
            occupied.update(s.positions)
        for _ in range(100):
            p = (random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1))
            if p not in occupied:
                self.position = p
                return
        self.position = (random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1))


# ── Visual helpers ─────────────────────────────────────────────────────────────

class TrailManager:
    """Stores recent grid positions for a snake and fades them each display frame."""

    def __init__(self, color):
        self.color  = color
        self._trail = deque(maxlen=TRAIL_LENGTH)   # each entry: [grid_pos, alpha]

    def record_move(self, grid_pos):
        self._trail.appendleft([grid_pos, TRAIL_START_ALPHA])

    def tick_fade(self):
        for entry in self._trail:
            entry[1] = max(0, entry[1] - TRAIL_FADE_PER_FRAME)

    def get_segments(self):
        return list(self._trail)  # [(pos, alpha), ...]

    def clear(self):
        self._trail.clear()


class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'alpha', 'color', 'radius', 'life')

    def __init__(self, x, y, color):
        angle   = random.uniform(0, 2 * math.pi)
        speed   = random.uniform(1.5, 4.5)
        self.x      = float(x)
        self.y      = float(y)
        self.vx     = math.cos(angle) * speed
        self.vy     = math.sin(angle) * speed
        self.alpha  = 255
        self.color  = color
        self.radius = random.randint(2, 5)
        self.life   = random.randint(20, 40)

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vx *= 0.93
        self.vy *= 0.93
        self.alpha = max(0, self.alpha - 255 // self.life)
        self.life -= 1
        return self.life > 0


class ParticleSystem:
    def __init__(self):
        self._particles = []

    def explode(self, grid_pos, color, count=18):
        px = grid_pos[0] * GRID_SIZE + GRID_SIZE // 2
        py = grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
        for _ in range(count):
            self._particles.append(Particle(px, py, color))

    def update_and_draw(self, surface):
        surviving = []
        for p in self._particles:
            if p.update():
                surviving.append(p)
                r, g, b = p.color
                col = (min(255, r), min(255, g), min(255, b), int(p.alpha))
                pygame.draw.circle(surface, col, (int(p.x), int(p.y)), p.radius)
        self._particles = surviving


# ── Pre-built static surfaces ──────────────────────────────────────────────────

def _build_grid_surface():
    surf = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
    for x in range(0, WINDOW_SIZE, GRID_SIZE):
        alpha = 55 if x % 100 == 0 else 35
        pygame.draw.line(surf, (*GRID_LINE_COL, alpha), (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, GRID_SIZE):
        alpha = 55 if y % 100 == 0 else 35
        pygame.draw.line(surf, (*GRID_LINE_COL, alpha), (0, y), (WINDOW_SIZE, y))
    return surf


def _build_scanline_surface():
    surf = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
    for y in range(0, WINDOW_SIZE, 2):
        pygame.draw.line(surf, (0, 0, 0, 18), (0, y), (WINDOW_SIZE, y))
    return surf


# ── NeonRenderer ──────────────────────────────────────────────────────────────

class NeonRenderer:
    """Owns the glow surface and drives all draw calls."""

    def __init__(self, screen):
        self.screen       = screen
        self.glow_surf    = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        self.grid_surf    = _build_grid_surface()
        self.scanline_surf = _build_scanline_surface()
        pygame.freetype.init()
        self._ft = pygame.freetype.Font(None, 36)

    # ── Public frame lifecycle ──────────────────────────────────────────────

    def begin_frame(self):
        self.screen.fill(NEON_BG)
        self.screen.blit(self.grid_surf, (0, 0))
        self.glow_surf.fill((0, 0, 0, 0))

    def commit_glow(self):
        self.screen.blit(self.glow_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    def commit_scanlines(self):
        self.screen.blit(self.scanline_surf, (0, 0))

    # ── Glow drawing helpers ────────────────────────────────────────────────

    def draw_glow_rect(self, surface, color, grid_pos, layers=GLOW_LAYERS, br=BORDER_RADIUS):
        r, g, b = color
        rect = pygame.Rect(
            grid_pos[0] * GRID_SIZE + 1,
            grid_pos[1] * GRID_SIZE + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2,
        )
        for i in range(layers, 0, -1):
            alpha   = int(180 / (i * 1.8))
            inflate = i * 3
            inflated = rect.inflate(inflate * 2, inflate * 2)
            pygame.draw.rect(surface, (r, g, b, alpha), inflated,
                             border_radius=br + inflate)
        # bright core
        pygame.draw.rect(surface, (r, g, b, 240), rect, border_radius=br)

    def draw_trail(self, trail_segments, color):
        r, g, b = color
        for pos, alpha in trail_segments:
            if alpha <= 0:
                continue
            rect = pygame.Rect(
                pos[0] * GRID_SIZE + 2,
                pos[1] * GRID_SIZE + 2,
                GRID_SIZE - 4,
                GRID_SIZE - 4,
            )
            pygame.draw.rect(self.glow_surf, (r, g, b, alpha), rect,
                             width=2, border_radius=BORDER_RADIUS)

    def draw_snake(self, positions, body_color, head_color):
        for i, pos in enumerate(positions):
            col = head_color if i == 0 else body_color
            self.draw_glow_rect(self.glow_surf, col, pos)

    def draw_food(self, position):
        t      = pygame.time.get_ticks() % 1000
        pulse  = math.sin(t / 1000 * 2 * math.pi)
        radius = int(GRID_SIZE // 2 + pulse * 4)
        bright = int(180 + pulse * 37.5)
        r, g, b = FOOD_CORE
        cx = position[0] * GRID_SIZE + GRID_SIZE // 2
        cy = position[1] * GRID_SIZE + GRID_SIZE // 2

        # glow rings
        for layer in range(4, 0, -1):
            alpha   = int(60 / layer)
            lr      = radius + layer * 3
            pygame.draw.circle(self.glow_surf,
                               (r, g, b, alpha), (cx, cy), lr)
        # bright core
        core_col = (min(255, bright), min(255, bright), min(255, int(b * 0.8)), 240)
        pygame.draw.circle(self.glow_surf, core_col, (cx, cy), radius)

    def draw_particles(self, particle_system):
        particle_system.update_and_draw(self.glow_surf)

    # ── HUD text (freetype, drawn above glow) ──────────────────────────────

    def draw_text(self, text, pos, size=30, color=(255, 255, 255)):
        self._ft.size = size
        # glow offsets
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1),
                   (-2, 0), (2, 0), (0, -2), (0, 2)]
        r, g, b = color
        for ox, oy in offsets:
            self._ft.render_to(self.screen, (pos[0] + ox, pos[1] + oy),
                               text, (min(255, r), min(255, g), min(255, b), 60))
        self._ft.render_to(self.screen, pos, text, color)

    def draw_text_centered(self, text, cy, size=36, color=(255, 255, 255)):
        self._ft.size = size
        rect, _ = self._ft.render(text, color)
        x = WINDOW_SIZE // 2 - rect.get_width() // 2
        self.draw_text(text, (x, cy), size=size, color=color)


# ── Menu ───────────────────────────────────────────────────────────────────────

def show_neon_menu(screen, clock):
    """
    Display the neon game-mode selection menu.
    Returns 'single', 'ai', or 'quit'.
    """
    renderer = NeonRenderer(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'single'
                elif event.key == pygame.K_2:
                    return 'ai'
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return 'quit'

        renderer.begin_frame()
        renderer.commit_glow()

        renderer.draw_text_centered('NEON SNAKE', 100, size=60, color=PLAYER_NEON)
        renderer.draw_text_centered('Choose Game Mode', 175, size=36, color=(200, 200, 255))
        renderer.draw_text_centered('1 - Single Player', 230, size=30, color=PLAYER_NEON)
        renderer.draw_text_centered('2 - Play Against Computer', 270, size=30, color=AI1_NEON)
        renderer.draw_text_centered('Q - Quit', 340, size=28, color=(140, 140, 180))

        renderer.commit_scanlines()
        pygame.display.update()
        clock.tick(FPS)


# ── Overlay helpers ────────────────────────────────────────────────────────────

def _draw_game_over(renderer, score):
    renderer.draw_text_centered('GAME OVER', WINDOW_SIZE // 2 - 60,
                                size=60, color=UI_GAMEOVER)
    renderer.draw_text_centered(f'Score: {score}', WINDOW_SIZE // 2,
                                size=36, color=(255, 200, 200))
    renderer.draw_text_centered('SPACE restart  ESC menu', WINDOW_SIZE // 2 + 50,
                                size=24, color=(160, 160, 200))


def _draw_pause(renderer):
    renderer.draw_text_centered('PAUSED', WINDOW_SIZE // 2 - 30,
                                size=60, color=PLAYER_NEON)
    renderer.draw_text_centered('P - continue', WINDOW_SIZE // 2 + 40,
                                size=28, color=(160, 160, 200))


# ── Single-player neon mode ────────────────────────────────────────────────────

def neon_single_player(screen, clock):
    renderer  = NeonRenderer(screen)
    particles = ParticleSystem()
    trail     = TrailManager(PLAYER_NEON)

    snake = SnakeLogic()
    food  = FoodLogic()
    food.randomize_position([snake])

    game_over   = False
    paused      = False
    move_counter = 0
    last_head   = snake.get_head_position()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position([snake])
                        trail.clear()
                        game_over    = False
                        move_counter = 0
                        last_head    = snake.get_head_position()
                    elif event.key == pygame.K_ESCAPE:
                        return
                elif paused:
                    if event.key == pygame.K_p:
                        paused = False
                else:
                    if event.key == pygame.K_UP    and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN  and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT  and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT
                    elif event.key == pygame.K_p:
                        paused = True
                    elif event.key == pygame.K_ESCAPE:
                        return

        if not game_over and not paused:
            move_counter += 1
            if move_counter >= PLAYER_MOVE_DELAY:
                move_counter = 0
                trail.record_move(last_head)
                if not snake.update():
                    particles.explode(snake.get_head_position(), PLAYER_NEON)
                    game_over = True
                else:
                    last_head = snake.get_head_position()
                    if snake.get_head_position() == food.position:
                        snake.length += 1
                        snake.score  += 1
                        food.randomize_position([snake])

        trail.tick_fade()

        renderer.begin_frame()
        renderer.draw_trail(trail.get_segments(), PLAYER_NEON)
        renderer.draw_snake(snake.positions, PLAYER_NEON, PLAYER_HEAD)
        renderer.draw_food(food.position)
        renderer.draw_particles(particles)
        renderer.commit_glow()

        renderer.draw_text(f'Score: {snake.score}', (10, 10), size=28, color=PLAYER_NEON)
        renderer.draw_text('P:Pause  ESC:Menu', (10, WINDOW_SIZE - 30),
                           size=20, color=(100, 100, 150))

        if game_over:
            _draw_game_over(renderer, snake.score)
        elif paused:
            _draw_pause(renderer)

        renderer.commit_scanlines()
        pygame.display.update()
        clock.tick(FPS)


# ── AI / multiplayer neon mode ─────────────────────────────────────────────────

def neon_ai_mode(screen, clock):
    renderer  = NeonRenderer(screen)
    particles = ParticleSystem()

    def _make_snakes():
        player = SnakeLogic()
        ai1    = ComputerSnakeLogic((5, 5))
        ai2    = ComputerSnakeLogic((GRID_COUNT - 6, 5))
        return player, [ai1, ai2]

    player_snake, ai_snakes = _make_snakes()
    all_snakes   = [player_snake] + ai_snakes
    food         = FoodLogic()
    food.randomize_position(all_snakes)

    ai_colors = [(AI1_NEON, AI1_HEAD), (AI2_NEON, AI2_HEAD)]

    player_trail = TrailManager(PLAYER_NEON)
    ai_trails    = [TrailManager(AI1_NEON), TrailManager(AI2_NEON)]

    game_over      = False
    paused         = False
    move_counter   = 0
    ai_move_counter = 0
    player_last    = player_snake.get_head_position()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        player_snake, ai_snakes = _make_snakes()
                        all_snakes = [player_snake] + ai_snakes
                        food.randomize_position(all_snakes)
                        player_trail.clear()
                        for t in ai_trails:
                            t.clear()
                        game_over       = False
                        move_counter    = 0
                        ai_move_counter = 0
                        player_last     = player_snake.get_head_position()
                    elif event.key == pygame.K_ESCAPE:
                        return
                elif paused:
                    if event.key == pygame.K_p:
                        paused = False
                else:
                    if event.key == pygame.K_UP    and player_snake.direction != DOWN:
                        player_snake.direction = UP
                    elif event.key == pygame.K_DOWN  and player_snake.direction != UP:
                        player_snake.direction = DOWN
                    elif event.key == pygame.K_LEFT  and player_snake.direction != RIGHT:
                        player_snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and player_snake.direction != LEFT:
                        player_snake.direction = RIGHT
                    elif event.key == pygame.K_p:
                        paused = True
                    elif event.key == pygame.K_ESCAPE:
                        return

        if not game_over and not paused:
            move_counter    += 1
            ai_move_counter += 1

            player_moved = move_counter >= PLAYER_MOVE_DELAY
            if player_moved:
                move_counter = 0
                player_trail.record_move(player_last)
                if not player_snake.update_with_collision_check(all_snakes):
                    particles.explode(player_snake.get_head_position(), PLAYER_NEON)
                    game_over = True
                    continue
                player_last = player_snake.get_head_position()

            ai_moved = ai_move_counter >= AI_MOVE_DELAY
            if ai_moved:
                ai_move_counter = 0
                for ai in ai_snakes:
                    ai.ai_move(food.position, all_snakes)

                dead_ai = []
                for idx, ai in enumerate(ai_snakes):
                    ai_trails[idx].record_move(ai.get_head_position())
                    if not ai.update_with_collision_check(all_snakes):
                        neon_col = ai_colors[idx % len(ai_colors)][0]
                        particles.explode(ai.get_head_position(), neon_col)
                        dead_ai.append((idx, ai))

                for idx, ai in reversed(dead_ai):
                    ai_snakes.pop(idx)
                    all_snakes.remove(ai)
                    ai_trails.pop(idx)
                    ai_colors.pop(idx)

                if not ai_snakes:
                    a1 = ComputerSnakeLogic((5, 5))
                    a2 = ComputerSnakeLogic((GRID_COUNT - 6, 5))
                    ai_snakes = [a1, a2]
                    ai_trails = [TrailManager(AI1_NEON), TrailManager(AI2_NEON)]
                    ai_colors = [(AI1_NEON, AI1_HEAD), (AI2_NEON, AI2_HEAD)]
                    all_snakes = [player_snake] + ai_snakes

            if player_moved or ai_moved:
                for snake in all_snakes:
                    if snake.get_head_position() == food.position:
                        snake.length += 1
                        if snake is player_snake:
                            snake.score += 1
                        food.randomize_position(all_snakes)
                        break

        player_trail.tick_fade()
        for t in ai_trails:
            t.tick_fade()

        renderer.begin_frame()

        renderer.draw_trail(player_trail.get_segments(), PLAYER_NEON)
        for idx, ai in enumerate(ai_snakes):
            renderer.draw_trail(ai_trails[idx].get_segments(),
                                ai_colors[idx % len(ai_colors)][0])

        renderer.draw_snake(player_snake.positions, PLAYER_NEON, PLAYER_HEAD)
        for idx, ai in enumerate(ai_snakes):
            nc, hc = ai_colors[idx % len(ai_colors)]
            renderer.draw_snake(ai.positions, nc, hc)

        renderer.draw_food(food.position)
        renderer.draw_particles(particles)
        renderer.commit_glow()

        renderer.draw_text(f'Score: {player_snake.score}', (10, 10),
                           size=28, color=PLAYER_NEON)
        renderer.draw_text(f'AI alive: {len(ai_snakes)}', (10, 40),
                           size=22, color=(180, 180, 220))
        renderer.draw_text('P:Pause  ESC:Menu', (10, WINDOW_SIZE - 30),
                           size=20, color=(100, 100, 150))

        if game_over:
            _draw_game_over(renderer, player_snake.score)
        elif paused:
            _draw_pause(renderer)

        renderer.commit_scanlines()
        pygame.display.update()
        clock.tick(FPS)


# ── Standalone entry point ─────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('Neon Snake')
    clock = pygame.time.Clock()

    while True:
        mode = show_neon_menu(screen, clock)
        if mode == 'single':
            neon_single_player(screen, clock)
        elif mode == 'ai':
            neon_ai_mode(screen, clock)
        else:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
