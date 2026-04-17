import pygame
import sys
from clock import MickeyClock

def main():
    pygame.init()
    
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    fps_clock = pygame.time.Clock()
    mickey_clock = MickeyClock(WIDTH // 2, HEIGHT // 2)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill((255, 255, 255))
        
        mickey_clock.draw(screen)
        
        pygame.display.flip()
        fps_clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()