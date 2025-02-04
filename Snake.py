import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# ----- Constants -----
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
FPS = 15  # Adjust speed here

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# Size of snake block and food
BLOCK_SIZE = 10

# Setup the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Font for text rendering
FONT = pygame.font.SysFont('Arial', 25)

# Clock for controlling the frame rate
clock = pygame.time.Clock()


def draw_text(text, font, color, surface, x, y):
    """Helper function to draw centered text."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_button(text, rect, color, text_color):
    """Helper function to draw a button with text."""
    pygame.draw.rect(screen, color, rect)
    text_surf = FONT.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def main_menu():
    """Display the main menu and wait for the player to click Start."""
    while True:
        screen.fill(BLACK)
        draw_text("Snake Game", FONT, GREEN, screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)

        # Define a start button rectangle
        start_button = pygame.Rect(WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2 - 25, 100, 50)
        draw_button("Start", start_button, BLUE, WHITE)

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_loop()  # Start the game

        pygame.display.update()
        clock.tick(FPS)


def game_loop():
    """Main game loop where the snake moves and the game is played."""
    # Initial snake setup
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction

    # Place initial food
    food_pos = [random.randrange(1, (WINDOW_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(1, (WINDOW_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
    food_spawn = True

    score = 0

    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handling key events for direction change
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Update the direction
        direction = change_to

        # Update snake position
        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        # Snake body growing mechanism:
        # Insert new head position and remove the tail unless food is eaten
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawn food if needed
        if not food_spawn:
            food_pos = [random.randrange(1, (WINDOW_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                        random.randrange(1, (WINDOW_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
        food_spawn = True

        # Fill the background
        screen.fill(BLACK)

        # Draw the snake
        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw the food
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # Check for collisions with boundaries
        if (snake_pos[0] < 0 or snake_pos[0] >= WINDOW_WIDTH or
            snake_pos[1] < 0 or snake_pos[1] >= WINDOW_HEIGHT):
            game_over(score)

        # Check for collision with itself
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(score)

        # Display the score
        score_text = FONT.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, [5, 5])

        pygame.display.update()
        clock.tick(FPS)


def game_over(score):
    """Display the game over screen with the final score and a Retry button."""
    while True:
        screen.fill(BLACK)
        draw_text("Game Over", FONT, RED, screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
        draw_text("Score: " + str(score), FONT, WHITE, screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 + 40)

        # Define a retry button rectangle
        retry_button = pygame.Rect(WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2 - 25, 100, 50)
        draw_button("Retry", retry_button, BLUE, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    game_loop()  # Restart the game

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()
