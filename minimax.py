from debug import DEBUG_2

# This function checks if a player has won the game
def check_win(game_board, side):
    rows = len(game_board)
    cols = len(game_board[0])

    # Check for 4 in a row in any column
    for col in range(cols):
        count = 0
        for row in range(rows):
            if game_board[row][col] == side:
                count += 1
                if count == 4:  # Found 4 in a row
                    print(f"Player {side} wins vertically in column {col}")
                    return True
            else:
                count = 0  # Reset count if the streak is broken

    # Check for 4 in a row in any row
    for row in range(rows):
        count = 0
        for col in range(cols):
            if game_board[row][col] == side:
                count += 1
                if count == 4:  # Found 4 in a row
                    print(f"Player {side} wins horizontally in row {row}")
                    return True
            else:
                count = 0  # Reset count if the streak is broken

    # Check for 4 in a row in any diagonal (top-left to bottom-right)
    for row in range(rows - 3):  # Ensure enough space for 4 in a row
        for col in range(cols - 3):
            if (game_board[row][col] == side and
                game_board[row + 1][col + 1] == side and
                game_board[row + 2][col + 2] == side and
                game_board[row + 3][col + 3] == side):
                print(f"Player {side} wins diagonally (\\) starting at row {row}, col {col}")
                return True

    # Check for 4 in a row in any diagonal (bottom-left to top-right)
    for row in range(3, rows):  # Start from row 3 to ensure enough space upwards
        for col in range(cols - 3):
            if (game_board[row][col] == side and
                game_board[row - 1][col + 1] == side and
                game_board[row - 2][col + 2] == side and
                game_board[row - 3][col + 3] == side):
                print(f"Player {side} wins diagonally (/) starting at row {row}, col {col}")
                return True

    return False


# Calculates the score for a given game board in place of a specific player
def evaluation(game_board, side):
    score = 0

    # Add weight for occupying center column
    score += center_weight(game_board, side)

    # Add score if the player is close to winning
    # Also reduce score if opponent is close to winning to encourage blocking
    # Add score for horizontal, vertical, and diagonal weights
    horizontal_score = horizontal_weight(game_board, side)
    vertical_score = vertical_weight(game_board, side)
    diagonal_l_score = diagonal_weight_l(game_board, side)
    diagonal_r_score = diagonal_weight_r(game_board, side)

    if DEBUG_2:
        print(f"Horizontal weight for side {side}: {horizontal_score}")
        print(f"Vertical weight for side {side}: {vertical_score}")
        print(f"Diagonal (\\) weight for side {side}: {diagonal_l_score}")
        print(f"Diagonal (/) weight for side {side}: {diagonal_r_score}")

    score += horizontal_score
    score += vertical_score
    score += diagonal_l_score
    score += diagonal_r_score

    return score


# Center column is more valuable as it allows more winning combinations
# This function add weight to center column and adjacent columns
def center_weight(game_board, side):
    rows = len(game_board)
    cols = len(game_board[0])
    weight = 0

    center_col = cols // 2

    for row in range(rows):
        # Check center most column
        if game_board[row][center_col] == side:
            weight += 3

        # Check adjacent columns
        elif center_col - 1 >= 0 and game_board[row][center_col - 1] == side:
            weight += 2
        elif center_col + 1 < cols and game_board[row][center_col + 1] == side:
            weight += 2
    return weight


# This function calculate weight to horizonal winning move 
def horizontal_weight(game_board, side):
    weight = 0
    rows = len(game_board)
    cols = len(game_board[0])

    for row in range(rows):
        # minus 3 to ensure the calculation is within the board limits
        for col in range(cols - 3):
            window = [game_board[row][col + i] for i in range(4)]
            weight += window_calculation(window, side)

    return weight


# This function calculate weight to vertical winning move
def vertical_weight(game_board, side):
    weight = 0
    rows = len(game_board)
    cols = len(game_board[0])

    for col in range(cols):
        # minus 3 to ensure the calculation is within the board limits
        for row in range(rows - 3):
            window = [game_board[row + i][col] for i in range(4)]
            weight += window_calculation(window, side)

    return weight


# This function calculate weight to diagonal winning move (top-left to bottom-right)
def diagonal_weight_l(game_board, side):
    weight = 0
    rows = len(game_board)
    cols = len(game_board[0])

    for row in range(rows - 3):
        for col in range(cols - 3):
            window = [game_board[row + i][col + i] for i in range(4)]
            weight += window_calculation(window, side)

    return weight


# This function calculate weight to diagonal winning move (bottom-left to top-right)
def diagonal_weight_r(game_board, side):
    weight = 0
    rows = len(game_board)
    cols = len(game_board[0])

    for row in range(3, rows):
        for col in range(cols - 3):
            window = [game_board[row - i][col + i] for i in range(4)]
            weight += window_calculation(window, side)

    return weight


# This function add weight according to how close the window is to winning
# Closer to winning, higher the score
# Also reduce weight if opponent is 1 move away from winning
def window_calculation(window, side):
    opponent = 1 if side == 2 else 2
    score = 0

    player_pieces = window.count(side)
    opponent_pieces = window.count(opponent)

    # Count empty spaces in the window
    empty_spaces = window.count(0)

    if player_pieces == 4: # Winning move
        score += 10000  
    elif player_pieces == 3 and empty_spaces == 1: # 1 move away from winning
        score += 100  
    elif player_pieces == 2 and empty_spaces == 2: # 2 move away from winning
        score += 10  

    if opponent_pieces == 3 and empty_spaces == 1: # Block opponent's winning move
        score -= 1000

    return score


# This function perform minimax algorithm to find the score for placing piece at each column
def minimax_move(game_board, side, depth):
    cols = len(game_board[0])

    # Determine the opponent's side
    opponent = 1 if side == 2 else 2  

    # Initialize scores for each column
    # Use a sufficiently large negative number
    scores = [-999999] * cols  

    # Calculate the score for each column
    for col in range(cols):
        # Check if the column is available to place a piece
        # If the column is full, assign a very low score to indicate it's not a good move
        if not column_avail(game_board, col):
            scores[col] = -999990
            continue

        # Simulate placing a piece in this column
        next_board = clone_and_place_piece(game_board, side, col)

        alpha = -1000000  # Use a sufficiently large negative number for alpha
        beta = 1000000    # Use a sufficiently large positive number for beta

        # Calculate the score for placing in this column using minimax with alpha-beta pruning
        # As maximizing player has already placed a piece, start with minimizing player's turn
        scores[col] = minimax(next_board, depth - 1, alpha, beta, False, side, opponent)

    return scores


# This function checks if a column is available to place piece, i.e. not full
def column_avail(game_board, column):
    if game_board[0][column] == 0: return True
    return False


# This function returns the available columns to place a piece
def columns_avail(game_board):
    cols = len(game_board[0])
    valid_columns = [col for col in range(cols) if column_avail(game_board, col)]
    return valid_columns


# This function simulates placing a piece in the game board at a specific column
def clone_and_place_piece(board, side, column):
    new_board = [row[:] for row in board]  # Deep copy of the board
    for row in reversed(range(len(board))):  # Start from the bottom row
        if new_board[row][column] == 0:
            new_board[row][column] = side
            
            if DEBUG_2: print(f"Placed piece for side {side} in column {column}, row {row}")
            break
    return new_board


# This function calculates the score for a given game board using minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player, side, opponent):
    valid_columns = columns_avail(board)
    is_terminal = check_win(board, side) or check_win(board, opponent) or len(valid_columns) == 0

    # Base case: terminal state or depth reached
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, side): # Maximizing player wins
                return 99999  
            elif check_win(board, opponent): # Opponent wins
                return -99999  
            else: # Draw
                return 0  
        else:
            eval_score = evaluation(board, side)
            if DEBUG_2: print(f"Evaluation score at depth {depth}: {eval_score}")
            return eval_score

    # if the next move is maximizing player's turn
    if maximizing_player: 
        # Start with a sufficiently large negative number
        max_eval = -999000 

        for col in valid_columns:
            # Simulate placing a piece in this column
            next_board = clone_and_place_piece(board, side, col)

            # Perform minimizing player's turn
            eval = minimax(next_board, depth - 1, alpha, beta, False, side, opponent)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    
    # if the next move is minimizing player's turn
    else: 
        # Start with a sufficiently large positive number
        min_eval = 999000

        for col in valid_columns:
            # Simulate placing a piece in this column
            next_board = clone_and_place_piece(board, opponent, col)

            # Perform maximizing player's turn
            eval = minimax(next_board, depth - 1, alpha, beta, True, side, opponent)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval