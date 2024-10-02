import numpy as np
import random
import pickle

def initialize_board():
    return [' '] * 9

def check_winner(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)

def check_draw(board):
    return ' ' not in board

def available_actions(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

def print_board(board):
    print("\n")
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("--+---+--")
    print("\n")


def minimax(board, depth, is_maximizing, ai_player, opponent_player):
    if check_winner(board, ai_player):
        return 1  
    elif check_winner(board, opponent_player):
        return -1  
    elif check_draw(board):
        return 0  

    if is_maximizing:
        best_score = -float('inf')
        for move in available_actions(board):
            board[move] = ai_player
            score = minimax(board, depth + 1, False, ai_player, opponent_player)
            board[move] = ' '  # Undo the move
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in available_actions(board):
            board[move] = opponent_player
            score = minimax(board, depth + 1, True, ai_player, opponent_player)
            board[move] = ' '  
            best_score = min(score, best_score)
        return best_score


def choose_minimax_action(board, ai_player, opponent_player):
    best_score = -float('inf')
    best_move = None
    for move in available_actions(board):
        board[move] = ai_player
        score = minimax(board, 0, False, ai_player, opponent_player)
        board[move] = ' ' 
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def play_game(ai_player='X', opponent_player='O', opponent_type='random'):
    board = initialize_board()
    current_player = 'X'

    while True:
        print_board(board)
        if current_player == ai_player:
            action = choose_minimax_action(board, ai_player, opponent_player)
        else:
            if opponent_type == 'ai':
                action = choose_minimax_action(board, opponent_player, ai_player)
            else:
                actions = available_actions(board)
                action = random.choice(actions)  # Random move for opponent

        board[action] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            return current_player
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            return 'Draw'

        current_player = 'O' if current_player == 'X' else 'X'

def play_against_ai():
    board = initialize_board()
    current_player = 'X'

    while True:
        print_board(board)
        if current_player == 'X':
            action = int(input("Enter your move (1-9): ")) - 1
            if board[action] != ' ':
                print("Invalid move. Try again.")
                continue
        else:
            action = choose_minimax_action(board, 'O', 'X')

        board[action] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    print("1. Play against the AI")
    choice = input("Choose an option (1): ")

    if choice == '1':
        play_against_ai()
    else:
        print("Invalid choice.")
