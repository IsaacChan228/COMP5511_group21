from flask import Flask, render_template, request, jsonify
from debug import DEBUG
import logging
import os

# create Flask environment
app = Flask(__name__)

##### Constants #####

# Constants for the game board dimensions
board_rows = 6
board_cols = 7

# Initialize the game board
game_board = [[0 for _ in range(board_cols)] for _ in range(board_rows)]

# Initialize the next-move cell
next_move_cell = 1

##### Routes for the main pages #####

@app.route('/')
def index():
    return render_template('index.html', game_board=game_board,
                            next_move_cell=next_move_cell, enumerate=enumerate)

@app.route('/update', methods=['POST'])


##### Gui Action Functions #####

def gameboard_update():
    # This function would update the GUI game board with the values from the game_board array
    global game_board
    if DEBUG: print("Game board updated.")

    return jsonify({'game_board': game_board})

@app.route('/cell-click', methods=['POST'])
def cell_click():
    # This function handles the cell click event from the GUI
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')

    if DEBUG: print(f"Cell clicked at row: {row}, column: {col}")

    # Call handler function with row and col as parameters
    result = handle_cell_click(row, col)

    return jsonify({'message': f'Cell at row {row}, column {col} processed.', 'result': result})

@app.route('/verify-state', methods=['POST'])
def state_verify_click():
    if DEBUG: print("Verifying game state")
    
    # Call handler function
    result = handle_state_verify()

    if result == 1: message = "Game state is valid"
    elif result == 2: message = "Invalid game state: Red has made more moves than Green"
    elif result == 3: message = "Invalid game state: Green has made more moves than Red"
    elif result == 4: message = "Invalid game state: Floating cell detected"
    else: message = "Unknown error"

    if DEBUG: print(f"Game state verification result: {message}")

    # Return the result to the frontend
    return jsonify({'message': message})

@app.route('/reset-board', methods=['POST'])
def reset_gameboard_click():
    reset_gameboard()
    if DEBUG: print("Game board has been reset.")
    return jsonify({'message': 'Game board has been reset.'})

@app.route('/nextmove-click', methods=['POST'])
def nextmove_click():
    if DEBUG: print("Next Move cell clicked")
    result=handle_next_move_click()
    return jsonify({'message': result})


##### Handler functions #####

def handle_cell_click(row, col):
    # This is a handler function that processes the cell click
    global game_board
    row = int(row)
    col = int(col)

    # Update the value based on the rules
    if game_board[row][col] == 0:
        game_board[row][col] = 1
    elif game_board[row][col] == 1:
        game_board[row][col] = 2
    elif game_board[row][col] == 2:
        game_board[row][col] = 0

    if DEBUG: print(f"Updated game_board[{row}][{col}] to {game_board[row][col]}")
    gameboard_update()

    return "Success"

def handle_state_verify():
    # This is a handler function that vertifies the game state
    global game_board

    # Check if the cell if any side has made extra moves (2 more than the other)
    count_1 = sum(row.count(1) for row in game_board)
    count_2 = sum(row.count(2) for row in game_board)
    if count_1 - count_2 > 1:
        return 2
    elif count_2 - count_1 > 1:
        return 3

    # Check if any cell is floating (1 or 2) without a cell below it
    for row in range(board_rows - 1):
        for col in range(board_cols):
            if game_board[row][col] != 0 and game_board[row + 1][col] == 0:
                return 4

    # Noraml state
    return 1

def reset_gameboard():
    # This function resets the game board to its initial state
    global game_board
    # Reset the game board to its initial state (all zeros)
    game_board = [[0 for _ in range(board_cols)] for _ in range(board_rows)]

    return 0

def handle_next_move_click():
    # This function handles the next move cell click event
    global next_move_cell

    # Update the next move cell value
    if next_move_cell == 0:
        next_move_cell = 1
    elif next_move_cell == 1:
        next_move_cell = 2
    elif next_move_cell == 2:
        next_move_cell = 1

    if DEBUG: print(f"Next move cell updated to {next_move_cell}")

    return "Success"


if __name__ == '__main__':
    app.run()