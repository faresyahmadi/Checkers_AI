import numpy as np
from copy import deepcopy
import random
import pickle
import os
from Checkers.constants import RED, WHITE
from minimax.algorithm import minimax, get_all_moves

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.q_table = {}  # State-action value table
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon  # Exploration rate

    def get_state_key(self, board):
        state = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece == 0:
                    state.append(0)
                else:
                    state.append(1 if piece.color == RED else 2)
        return tuple(state)

    def get_action(self, board, valid_moves):
        state = self.get_state_key(board)

        if random.random() < self.epsilon:
            return random.choice(list(valid_moves.items()))

        best_value = float('-inf')
        best_action = None

        for move, skip in valid_moves.items():
            action_key = (state, move)
            if action_key not in self.q_table:
                self.q_table[action_key] = 0

            if self.q_table[action_key] > best_value:
                best_value = self.q_table[action_key]
                best_action = (move, skip)

        return best_action if best_action else random.choice(list(valid_moves.items()))

    def update(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        action_key = (state_key, action)

        if action_key not in self.q_table:
            self.q_table[action_key] = 0

        next_state_key = self.get_state_key(next_state)
        next_max_q = max([self.q_table.get((next_state_key, a), 0)
                          for a in self.get_all_possible_actions(next_state)], default=0)

        current_q = self.q_table[action_key]
        self.q_table[action_key] = current_q + self.learning_rate * (
            reward + self.discount_factor * next_max_q - current_q)

    def get_all_possible_actions(self, board):
        actions = []
        for piece in board.get_all_pieces(RED):
            valid_moves = board.get_valid_moves(piece)
            actions.extend(valid_moves.keys())
        return actions

    def save_q_table(self, filename='q_table.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename='q_table.pkl'):
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print("No saved Q-table found. Starting with empty table.")


def load_training_stats(filename='training_stats.pkl'):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        return {'rl_agent_wins': 0, 'minimax_wins': 0, 'draws': 0}


def save_training_stats(stats, filename='training_stats.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(stats, f)


def train_against_minimax(episodes=1000, save_interval=100):
    print("\nStarting RL Agent Training...")
    print("--------------------------------")
    agent = QLearningAgent()
    agent.load_q_table()

    stats = load_training_stats()

    session_rl_agent_wins = 0
    session_minimax_wins = 0
    session_draws = 0

    for episode in range(episodes):
        from Checkers.game import Game
        game = Game(None)
        total_reward = 0
        moves = 0
        max_moves = 60

        while game.winner() is None and moves < max_moves:
            if game.turn == RED:
                valid_moves = {}
                for piece in game.board.get_all_pieces(RED):
                    valid_moves.update(game.board.get_valid_moves(piece))

                if not valid_moves:
                    break

                action, _ = agent.get_action(game.board, valid_moves)

                for piece in game.board.get_all_pieces(RED):
                    piece_valid_moves = game.board.get_valid_moves(piece)
                    if action in piece_valid_moves:
                        skip = piece_valid_moves[action]
                        game.board.move(piece, action[0], action[1])
                        if skip:
                            game.board.remove(skip)
                        game.change_turn()
                        break

                reward = calculate_reward(game)
                total_reward += reward
                moves += 1
                agent.update(game.board, action, reward, game.board)

            else:
                value, new_board = minimax(game.get_board(), 1, WHITE, game)
                if new_board is not None:
                    game.ai_move(new_board)
                    moves += 1
                else:
                    break

        winner = game.winner()
        if moves >= max_moves:
            session_draws += 1
            winner_text = "Draw (Max Moves)"
        else:
            if winner == RED:
                session_rl_agent_wins += 1
                winner_text = "RL Agent"
            elif winner == WHITE:
                session_minimax_wins += 1
                winner_text = "Minimax"
            else:
                session_draws += 1
                winner_text = "Draw"

        print(f"Episode {episode + 1}/{episodes} | Reward: {total_reward} | Moves: {moves} | Winner: {winner_text}")

        if (episode + 1) % save_interval == 0:
            agent.save_q_table()
            print("--------------------------------")

    # Update and save cumulative stats
    stats['rl_agent_wins'] += session_rl_agent_wins
    stats['minimax_wins'] += session_minimax_wins
    stats['draws'] += session_draws

    save_training_stats(stats)

    print("\nTraining Complete!")
    print(f"Final Q-table size: {len(agent.q_table)} entries")
    print("--------------------------------")
    print(f"Cumulative Stats so far:")
    print(f"RL Agent Wins: {stats['rl_agent_wins']}")
    print(f"Minimax Wins: {stats['minimax_wins']}")
    print(f"Draws: {stats['draws']}")
    return agent


def calculate_reward(game):
    if game.winner() == RED:
        return 100
    elif game.winner() == WHITE:
        return -100

    red_pieces = len(game.board.get_all_pieces(RED))
    white_pieces = len(game.board.get_all_pieces(WHITE))

    capture_reward = (white_pieces - red_pieces) * 10

    red_kings = sum(1 for piece in game.board.get_all_pieces(RED) if piece.king)
    white_kings = sum(1 for piece in game.board.get_all_pieces(WHITE) if piece.king)
    king_reward = (red_kings - white_kings) * 5

    return capture_reward + king_reward
