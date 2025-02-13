import pygame
import sys

def welcome_screen(win, width, height):

    # Define colors for buttons and text
    BLUE = (0, 122, 204)
    RED = (204, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255,255,0)

    # Set up font
    font = pygame.font.SysFont(None, 48)

    # Define button rectangles
    play_button = pygame.Rect(width // 2 - 100, height // 2 - 60, 200, 50)
    quit_button = pygame.Rect(width // 2 - 100, height // 2 + 10, 200, 50)

    # Load and scale background image
    try:
        background = pygame.image.load('assets/background.jpg')
        background = pygame.transform.scale(background, (width, height))
    except pygame.error as e:
        print("Background image not found or error loading image:", e)
        background = None

    # Load and play background music (ensure the file exists or update the path)
    try:
        pygame.mixer.music.load('assets/non.mp3')
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except pygame.error as e:
        print("Music file not found or error loading music:", e)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the Play button was clicked
                if play_button.collidepoint(event.pos):
                    return 
                # Check if the Quit button was clicked
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw the background image if loaded; otherwise, fill with a fallback color
        if background:
            win.blit(background, (0, 0))
        else:
            win.fill((0, 0, 0))  # Fallback: fill with black

        # Display title text
        title_text = font.render("Welcome to Fares Checkers", True,YELLOW)
        title_rect = title_text.get_rect(center=(width // 2, height // 2 - 150))
        win.blit(title_text, title_rect)

        # Draw the Play button
        pygame.draw.rect(win, BLUE, play_button)
        play_text = font.render("Play", True, WHITE)
        play_rect = play_text.get_rect(center=play_button.center)
        win.blit(play_text, play_rect)

        # Draw the Quit button
        pygame.draw.rect(win, RED, quit_button)
        quit_text = font.render("Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=quit_button.center)
        win.blit(quit_text, quit_rect)

        pygame.display.flip()
