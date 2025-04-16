from flask import jsonify
from debug import DEBUG_1
from display import display_tree
import minimax
import json
import math


# This function updates the game board and returns the updated game board
def gameboard_update(game_board):
    if DEBUG_1: print("Game board updated.")
    return jsonify({'game_board': game_board})


# This is a handler function that processes the cell click event
def handle_cell_click(row, col, game_board):
    row = int(row)
    col = int(col)

    # Update the value based on the rules
    if game_board[row][col] == 0:
        game_board[row][col] = 1
    elif game_board[row][col] == 1:
        game_board[row][col] = 2
    elif game_board[row][col] == 2:
        game_board[row][col] = 0

    if DEBUG_1: print(f"Updated game_board[{row}][{col}] to {game_board[row][col]}")
    gameboard_update(game_board)

    return "Success"


# This function inverts the game board values
def invert_game_board(game_board):
    for row in range(len(game_board)):
        for col in range(len(game_board[0])):
            if game_board[row][col] == 1:
                game_board[row][col] = 3
            elif game_board[row][col] == 2:
                game_board[row][col] = 1
        for col in range(len(game_board[0])):
            if game_board[row][col] == 3:
                game_board[row][col] = 2
    if DEBUG_1: print("Inverted game board:", game_board)


# This is a handler function that vertifies the game state
def handle_state_verify(game_board, next_move):
    # Check if any cell is floating (1 or 2) without a cell below it
    for row in range(len(game_board) - 1):
        for col in range(len(game_board[0])):
            if game_board[row][col] != 0 and game_board[row + 1][col] == 0:
                return 6

    # Check if the cell if any side has made extra moves (2 more than the other)
    count_1 = sum(row.count(1) for row in game_board)
    count_2 = sum(row.count(2) for row in game_board)
    if count_1 - count_2 > 1:
        return 2
    elif count_2 - count_1 > 1:
        return 3
    
    # Check if the next move cell is valid, i.e. if next move will cause an invalid state
    elif count_1 - count_2 == 1 and next_move == 1:
        return 4
    elif count_2 - count_1 == 1 and next_move == 2:
        return 5
    
    # Check if the any side is winning
    win_1 = minimax.check_win(game_board, 1)
    win_2 = minimax.check_win(game_board, 2)
    if win_1 and win_2:
        return 7
    if win_1:
        return 8
    elif win_2:
        return 9

    # Normal state
    return 1


# This function resets the game board to its initial state
def reset_gameboard(game_board):
    for row in range(len(game_board)):
        for col in range(len(game_board[0])):
            game_board[row][col] = 0
    return "Success"


# This function handles the next move cell click event
def handle_next_move_click(next_move):
    # Update the next move cell value
    if next_move == 0:
        next_move = 1
    elif next_move == 1:
        next_move = 2
    elif next_move == 2:
        next_move = 1

    if DEBUG_1: print(f"Next move cell updated to {next_move}")

    return next_move


# This function handles the minimax calculation and exports the minimax tree to a JSON file
def handle_minimax(game_board, next_move):
    # Set the depth for minimax calculation
    depth = 3

    # Dictionary to store the minimax tree
    minimax_tree = {}

    # Calculate the minimax scores for each column
    scores = minimax.minimax_move(game_board, next_move, depth, minimax_tree)

    # Replace math.inf, -math.inf, and "NA" in scores for display purposes
    scores = [
        "win" if score == math.inf else
        "lose" if score == -math.inf else
        "NA" if score == "NA" else score
        for score in scores
    ]

    # Replace math.inf and -math.inf in the minimax tree
    def replace_inf_in_tree(tree):
        for key, value in tree.items():
            if isinstance(value, dict):
                replace_inf_in_tree(value)  # Recursively replace in children
            elif key == "score":
                if value == math.inf:
                    tree[key] = "win"
                elif value == -math.inf:
                    tree[key] = "lose"

    replace_inf_in_tree(minimax_tree)

    # Export the minimax tree to a JSON file
    with open('minimax_tree.json', 'w') as jsonfile:
        json.dump(minimax_tree, jsonfile, indent=4)

    if DEBUG_1: print(f"Minimax tree exported to minimax_tree.json")

    return scores