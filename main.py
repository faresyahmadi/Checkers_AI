import pygame
pygame.init()
import sys
from Checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from Checkers.board import Board
from Checkers.game import Game
from minimax.algorithm import minimax
from Checkers.welcome import welcome_screen
from RL_algorithm import QLearningAgent, train_against_minimax

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fares Checkers')

def get_row_col_from_mouse(pos): 
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main(): 
    game_mode = welcome_screen(WIN, WIDTH, HEIGHT)
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    rl_agent = None
    if game_mode == 'train rl':
        print("\nInitializing training...")
        sys.stdout.flush()
        rl_agent = train_against_minimax(episodes=1000)
        print("\nTraining complete! Switching to play mode...")
        sys.stdout.flush()
        game_mode = 'rl vs player'
    elif game_mode == 'rl vs player':
        rl_agent = QLearningAgent()
        rl_agent.load_q_table()

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            if game_mode == 'ai vs player':
                value, new_board = minimax(game.get_board(), 3, WHITE, game, float('-inf'), float('inf'))
                game.ai_move(new_board)
            elif game_mode == 'rl vs player' and rl_agent:
                valid_moves = {}
                for piece in game.board.get_all_pieces(WHITE):
                    valid_moves.update(game.board.get_valid_moves(piece))

                if valid_moves:
                    action, _ = rl_agent.get_action(game.board, valid_moves)

                    for piece in game.board.get_all_pieces(WHITE):
                        piece_valid_moves = game.board.get_valid_moves(piece)
                        if action in piece_valid_moves:
                            skip = piece_valid_moves[action]  # <-- Re-fetch skip correctly
                            game.board.move(piece, action[0], action[1])
                            if skip:
                                game.board.remove(skip)
                            game.change_turn()
                            break

        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

if __name__ == "__main__":
    main()
