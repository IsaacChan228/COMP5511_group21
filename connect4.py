from flask import Flask, render_template, request, jsonify
from debug import DEBUG
import handler

# create Flask environment
app = Flask(__name__)


# Constants

# Constants for the game board dimensions
board_rows = 6
board_cols = 7

# Initialize the game board
game_board = [[0 for _ in range(board_cols)] for _ in range(board_rows)]

# Initialize the next-move cell
next_move = 1


# Routes for the GUI pages

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

    if DEBUG: print(f"Cell clicked at row: {row}, column: {col}")

    # Call handler function
    result = handler.handle_cell_click(row, col, game_board)
    if DEBUG: print(f"Cell click result: {result}")

    return jsonify({'message': f'Cell at row {row}, column {col} processed.', 'result': result})


# This function handles the invert state event from the GUI
@app.route('/invert-state', methods=['POST'])
def invert_state():
    global game_board
    handler.invert_game_board(game_board)  # Call the handler function to invert the board
    if DEBUG: print("Game board state inverted.")
    return jsonify({'message': 'Game board state inverted.'})


## This function handles the vertify state event from the GUI
@app.route('/verify-state', methods=['POST'])
def state_verify_click():
    if DEBUG: print("Verifying game state")
    
    # Call handler function
    result = handler.handle_state_verify(game_board, next_move)

    if result == 1: message = "Game state is valid"
    elif result == 2: message = "Invalid game state: Red has made more moves than Green"
    elif result == 3: message = "Invalid game state: Green has made more moves than Red"
    elif result == 4: message = "Invalid game state: Red's turn but Red has made the last move"
    elif result == 5: message = "Invalid game state: Green's turn but Green has made the last move"
    elif result == 6: message = "Invalid game state: Floating cell detected"
    elif result == 7: message = "Invalid game state: both side has winned"
    elif result == 8: message = "game state: Red wins"
    elif result == 9: message = "game state: Green wins"

    else: message = "Unknown error"

    if DEBUG: print(f"Game state verification result: {message}")

    # Return the result to the frontend
    return jsonify({'message': message})


## This function handles the reset game board event from the GUI
@app.route('/reset-board', methods=['POST'])
def reset_gameboard_click():
    result=handler.reset_gameboard(game_board)
    if DEBUG: print("Game board reset result:", result)

    # Return the result to the frontend   
    return jsonify({'message': 'Game board has been reset.'})


## This function handles the next move cell click event from the GUI
@app.route('/nextmove-click', methods=['POST'])
def nextmove_click():
    global next_move
    if DEBUG: print("Next Move cell clicked")
    next_move = handler.handle_next_move_click(next_move)

    # Return the result to the frontend  
    return jsonify({'message': 'Next move updated.', 'next_move': next_move})


if __name__ == '__main__':
    app.run()