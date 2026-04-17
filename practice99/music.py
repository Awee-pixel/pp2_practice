import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 24)

playlist = [
    "music1.mp3",
    "song2.mp3",
    "song3.mp3"
]

current_track = 0
playing = False

def load_track(index):
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    return True

def draw_ui():
    screen.fill((30, 30, 30))

    track_text = font.render(f"Track: {os.path.basename(playlist[current_track])}", True, (255, 255, 255))
    screen.blit(track_text, (20, 50))
    status = "Playing" if playing else "Stopped"
    status_text = font.render(f"Status: {status}", True, (200, 200, 200))
    screen.blit(status_text, (20, 100))

    controls = "P=Play S=Stop N=Next B=Back Q=Quit"
    control_text = font.render(controls, True, (150, 150, 150))
    screen.blit(control_text, (20, 200))

    pygame.display.flip()

def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    load_track(current_track)

def prev_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    load_track(current_track)

running = True
clock = pygame.time.Clock()

while running:
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Play
                load_track(current_track)
                playing = True

            elif event.key == pygame.K_s:  # Stop
                pygame.mixer.music.stop()
                playing = False

            elif event.key == pygame.K_n:  # Next
                next_track()
                playing = True

            elif event.key == pygame.K_b:  # Previous
                prev_track()
                playing = True

            elif event.key == pygame.K_q:  # Quit
                running = False

    clock.tick(30)

pygame.quit()