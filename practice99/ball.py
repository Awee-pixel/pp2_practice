import pygame

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball settings
radius = 25
x = WIDTH // 2
y = HEIGHT // 2
step = 20

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # Draw ball
    pygame.draw.circle(screen, RED, (x, y), radius)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Move Up
            if event.key == pygame.K_UP:
                if y - step - radius >= 0:
                    y -= step

            # Move Down
            elif event.key == pygame.K_DOWN:
                if y + step + radius <= HEIGHT:
                    y += step

            # Move Left
            elif event.key == pygame.K_LEFT:
                if x - step - radius >= 0:
                    x -= step

            # Move Right
            elif event.key == pygame.K_RIGHT:
                if x + step + radius <= WIDTH:
                    x += step

    pygame.display.flip()
    clock.tick(60)

pygame.quit()