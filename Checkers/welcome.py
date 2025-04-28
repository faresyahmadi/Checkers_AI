import pygame
import sys

def welcome_screen(win, width, height):

    
    BLUE = (0, 122, 204)
    RED = (204, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255,255,0)
    GREEN = (0, 0, 255)
    PURPLE = (128, 0, 128)

    
    font = pygame.font.SysFont(None, 48)

    
    play_button = pygame.Rect(width // 2 - 100, height // 2 - 180, 400, 50)
    ai_button = pygame.Rect(width // 2 - 100, height // 2 - 110, 400, 50)
    rl_train_button = pygame.Rect(width // 2 - 100, height // 2 - 40, 400, 50)
    rl_play_button = pygame.Rect(width // 2 - 100, height // 2 + 30, 400, 50)
    quit_button = pygame.Rect(width // 2 - 100, height // 2 + 100, 400, 50)

    
    try:
        background = pygame.image.load('assets/background.jpg')
        background = pygame.transform.scale(background, (width, height))
    except pygame.error as e:
        print("Background image not found or error loading image:", e)
        background = None

    
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
                
                if play_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return "player vs player"
                if ai_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return "ai vs player"
                if rl_train_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return "train rl"
                if rl_play_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return "rl vs player"
              
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if background:
            win.blit(background, (0, 0))
        else:
            win.fill((0, 0, 0))  

        title_text = font.render("Welcome to Fares Checkers", True,YELLOW)
        title_rect = title_text.get_rect(center=(width // 2, height // 2 - 250))
        win.blit(title_text, title_rect)

        pygame.draw.rect(win, BLUE, play_button)
        play_text = font.render("Player vs Player", True, WHITE)
        play_rect = play_text.get_rect(center=play_button.center)
        win.blit(play_text, play_rect)

        pygame.draw.rect(win, GREEN, ai_button)
        ai_text = font.render("Computer vs Player", True, WHITE)
        ai_rect = ai_text.get_rect(center=ai_button.center)
        win.blit(ai_text, ai_rect)

        pygame.draw.rect(win, PURPLE, rl_train_button)
        rl_train_text = font.render("Train RL Agent", True, WHITE)
        rl_train_rect = rl_train_text.get_rect(center=rl_train_button.center)
        win.blit(rl_train_text, rl_train_rect)

        pygame.draw.rect(win, PURPLE, rl_play_button)
        rl_play_text = font.render("Play vs RL Agent", True, WHITE)
        rl_play_rect = rl_play_text.get_rect(center=rl_play_button.center)
        win.blit(rl_play_text, rl_play_rect)

        pygame.draw.rect(win, RED, quit_button)
        quit_text = font.render("Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=quit_button.center)
        win.blit(quit_text, quit_rect)

        pygame.display.flip()
