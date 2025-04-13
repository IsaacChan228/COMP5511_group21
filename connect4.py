from flask import Flask, render_template, request, jsonify
from debug import DEBUG_0
import handler

# create Flask environment
app = Flask(__name__)


### Constants ###

# Constants for the game board dimensions
board_rows = 6
board_cols = 7

# Initialize the game board
game_board = [[0 for _ in range(board_cols)] for _ in range(board_rows)]

# Initialize the next-move cell
next_move = 1

# Global dictionary for state error messages
STATE_ERROR_MESSAGES = {
    1: "Game state is valid",
    2: "Invalid game state: Red has made more moves than Green",
    3: "Invalid game state: Green has made more moves than Red",
    4: "Invalid game state: Red's turn but Red has made the last move",
    5: "Invalid game state: Green's turn but Green has made the last move",
    6: "Invalid game state: Floating cell detected",
    7: "Invalid game state: Both sides have won",
    8: "Game state: Red wins",
    9: "Game state: Green wins",
}


### Routes for the GUI pages ###

@app.route('/')
def index():
    return render_template('index.html', game_board=game_board,
                            next_move=next_move, enumerate=enumerate)


# This function would update the GUI game board with the values from the game_board array
@app.route('/update', methods=['POST'])
def update():
    return jsonify({'game_board': game_board, 'next_move': next_move})


# This function handles the cell click event from the GUI
@app.route('/cell-click', methods=['POST'])
def cell_click():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')

    if DEBUG_0: print(f"Cell clicked at row: {row}, column: {col}")

    # Call handler function
    result = handler.handle_cell_click(row, col, game_board)
    if DEBUG_0: print(f"Cell click result: {result}")

    return jsonify({'message': f'Cell at row {row}, column {col} processed.', 'result': result})


# This function handles the invert state event from the GUI
@app.route('/invert-state', methods=['POST'])
def invert_state():
    global game_board
    handler.invert_game_board(game_board)  # Call the handler function to invert the board
    if DEBUG_0: print("Game board state inverted.")
    return jsonify({'message': 'Game board state inverted.'})


## This function handles the vertify state event from the GUI
@app.route('/verify-state', methods=['POST'])
def state_verify_click():
    if DEBUG_0: print("Verifying game state")
    
    # Call handler function
    result = handler.handle_state_verify(game_board, next_move)

    # Get the message from the global dictionary
    message = STATE_ERROR_MESSAGES.get(result, "Unknown error")

    if DEBUG_0: print(f"Game state verification result: {message}")

    # Return the result to the frontend
    return jsonify({'message': message})


## This function handles the reset game board event from the GUI
@app.route('/reset-board', methods=['POST'])
def reset_gameboard_click():
    result=handler.reset_gameboard(game_board)
    if DEBUG_0: print("Game board reset result:", result)

    # Return the result to the frontend   
    return jsonify({'message': 'Game board has been reset.'})


## This function handles the next move cell click event from the GUI
@app.route('/nextmove-click', methods=['POST'])
def nextmove_click():
    global next_move
    if DEBUG_0: print("Next Move cell clicked")
    next_move = handler.handle_next_move_click(next_move)

    # Return the result to the frontend  
    return jsonify({'message': 'Next move updated.', 'next_move': next_move})


# This function handles the minimax calculation event from the GUI
@app.route('/minimax', methods=['POST'])
def minimax_calculate():
    global game_board, next_move

    # Verify the game state before performing minimax calculation
    state_result = handler.handle_state_verify(game_board, next_move)

    # If the state is invalid, return an error message
    if state_result != 1:  # 1 indicates a valid state
        message = STATE_ERROR_MESSAGES.get(state_result, "Unknown error")
        if DEBUG_0: print(f"Invalid game state detected: {message}")
        return jsonify({'message': message, 'scores': []})

    # Call the handler function to calculate minimax scores and export the tree
    scores = handler.handle_minimax(game_board, next_move)

    if DEBUG_0: print(f"Minimax scores: {scores}")

    # Return the scores to the frontend
    return jsonify({'message': 'Minimax calculation complete.', 'scores': scores})


if __name__ == '__main__':
    app.run()