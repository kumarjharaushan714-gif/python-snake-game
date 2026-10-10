import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
CELL_SIZE = 20
COLS = 30
ROWS = 25
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Snake Game")

clock = pygame.time.Clock()

# Colors
BLACK = (18, 18, 25)
GREEN = (50, 220, 100)
DARK_GREEN = (20, 150, 70)
RED = (255, 70, 80)
WHITE = (245, 245, 245)
GRAY = (100, 100, 115)
GOLD = (255, 210, 60)

# Fonts
font = pygame.font.SysFont("consolas", 24, bold=True)
small_font = pygame.font.SysFont("consolas", 17)
big_font = pygame.font.SysFont("consolas", 42, bold=True)


def new_food(snake):
    while True:
        food = (
            random.randrange(COLS),
            random.randrange(ROWS)
        )
        if food not in snake:
            return food


def draw_cell(position, color, radius=4):
    x, y = position
    rect = pygame.Rect(
        x * CELL_SIZE,
        y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )
    pygame.draw.rect(screen, color, rect.inflate(-2, -2),
                     border_radius=radius)


def draw_game(snake, food, score, best_score):
    screen.fill(BLACK)

    # Draw food
    draw_cell(food, RED, 8)

    # Draw snake
    for index, segment in enumerate(snake):
        color = GREEN if index == 0 else DARK_GREEN
        draw_cell(segment, color)

    # Score panel
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    best_text = small_font.render(
        f"BEST: {best_score}", True, GOLD
    )

    screen.blit(score_text, (10, 8))
    screen.blit(best_text, (WIDTH - best_text.get_width() - 10, 13))

    pygame.display.flip()


def show_message(title, subtitle):
    screen.fill(BLACK)

    title_surface = big_font.render(title, True, GREEN)
    subtitle_surface = font.render(subtitle, True, WHITE)

    screen.blit(
        title_surface,
        title_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 35)
        )
    )
    screen.blit(
        subtitle_surface,
        subtitle_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 25)
        )
    )

    pygame.display.flip()


def main():
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    next_direction = direction

    food = new_food(snake)
    score = 0
    best_score = 0
    game_over = False
    won = False

    show_message("SNAKE GAME", "Press any arrow key to start")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if game_over:
                    if event.key == pygame.K_r:
                        return main()
                    elif event.key == pygame.K_q:
                        running = False
                    continue

                # Prevent reversing directly into yourself
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        if not running:
            break

        if game_over:
            message = "YOU WIN!" if won else "GAME OVER!"
            show_message(
                message,
                f"Score: {score} | R: Restart | Q: Quit"
            )
            clock.tick(15)
            continue

        direction = next_direction

        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if not (0 <= new_head[0] < COLS and
                0 <= new_head[1] < ROWS):
            game_over = True
            continue

        eating = new_head == food

        # Moving into the tail's current cell is allowed
        # when the tail moves away on the same turn.
        collision_body = snake if eating else snake[:-1]

        if new_head in collision_body:
            game_over = True
            continue

        snake.insert(0, new_head)

        if eating:
            score += 10
            best_score = max(best_score, score)

            if len(snake) == COLS * ROWS:
                won = True
                game_over = True
            else:
                food = new_food(snake)
        else:
            snake.pop()

        draw_game(snake, food, score, best_score)

        # Snake gets faster as the score increases
        speed = min(20, 10 + score // 50)
        clock.tick(speed)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()