# Import the pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()