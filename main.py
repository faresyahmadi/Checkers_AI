import pygame
pygame.init()
from Checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from Checkers.board import Board
from Checkers.game import Game
from minimax.algorithm import minimax
from Checkers.welcome import welcome_screen


FPS = 60
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Fares Checkers')

def get_row_col_from_mouse(pos): 
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row,col

def main(): 

    welcome_screen (WIN, WIDTH, HEIGHT)
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    while run: 

        ### MINIMAX IMPLEMENTATION ### 
        if game.turn == WHITE: 
            value, new_board = minimax(game.get_board(), 3, WHITE, game)
            game.ai_move(new_board)
        

        clock.tick(FPS)

        if game.winner != None: 
            print (game.winner())
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row,col = get_row_col_from_mouse(pos)                    
                game.select(row,col)


        game.update()
                  
    pygame.quit()

main()