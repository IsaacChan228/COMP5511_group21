from debug import DEBUG_2
import weight
import math

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
                    if DEBUG_2: print(f"Player {side} wins vertically in column {col}")
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
                    if DEBUG_2: print(f"Player {side} wins horizontally in row {row}")
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
                if DEBUG_2: print(f"Player {side} wins diagonally (\\) starting at row {row}, col {col}")
                return True

    # Check for 4 in a row in any diagonal (bottom-left to top-right)
    for row in range(3, rows):  # Start from row 3 to ensure enough space upwards
        for col in range(cols - 3):
            if (game_board[row][col] == side and
                game_board[row - 1][col + 1] == side and
                game_board[row - 2][col + 2] == side and
                game_board[row - 3][col + 3] == side):
                if DEBUG_2: print(f"Player {side} wins diagonally (/) starting at row {row}, col {col}")
                return True

    return False


# Calculates the score for a given game board in place of a specific player
def evaluation(game_board, side):
    score = 0

    # Center column is more valuable as it allows more winning combinations
    # Add score for occupying center column
    score += center_score(game_board, side)

    h_array = horizontal_weight(game_board, side)
    v_array = vertical_weight(game_board, side)
    d_l_array = diagonal_weight_l(game_board, side)
    d_r_array = diagonal_weight_r(game_board, side)

    if DEBUG_2:
        print(f"Horizontal progress for side {side}: {h_array}")
        print(f"Vertical progress for side {side}: {v_array}")
        print(f"Diagonal (\\) progress for side {side}: {d_l_array}")
        print(f"Diagonal (/) progress for side {side}: {d_r_array}")


    # Initialize total array to store total counts of 3-piece, 2-piece, etc.
    total_array = [0, 0, 0, 0]

    # Add counts from horizontal, vertical, and diagonal weights
    total_array = add_arrays(total_array, h_array)
    total_array = add_arrays(total_array, v_array)
    total_array = add_arrays(total_array, d_l_array)
    total_array = add_arrays(total_array, d_r_array)

    # Calculate score based on the total array
    # 4-piece: Winning move
    score += total_array[0] * weight.winning_move_4p
    # 3-piece: 1 move away from winning
    score += total_array[1] * weight.winning_move_3p
    # 2-piece: 2 moves away from winning
    score += total_array[2] * weight.winning_move_2p
    # 3 opponent piece: 1 move away from losing
    score += total_array[3] * weight.losing_move_3p

    # if the move can achieve multiple winning combinations,
    # provide a bonus score
    # No bonus score if opponent achieve 
    # multiple winning combinations, as it means losing
    if total_array[0] > 1: score += weight.m_winning_move_4p
    if total_array[1] > 1: score += weight.m_winning_move_3p
    if total_array[2] > 1: score += weight.m_winning_move_2p

    if DEBUG_2:
        print(f"Score for side {side}: {score}")
        print(f"Total array: {total_array}")
        print(f"game_board: {game_board}")

    return score


# Center column is more valuable as it allows more winning combinations
# This function add score to center column and adjacent columns
def center_score(game_board, side):
    rows = len(game_board)
    cols = len(game_board[0])
    score = 0

    center_col = cols // 2

    for row in range(rows):
        # Check center most column
        if game_board[row][center_col] == side:
            score += weight.center_col_merit

        # Check adjacent columns
        elif center_col - 1 >= 0 and game_board[row][center_col - 1] == side:
            score += weight.adj_col_merit
        elif center_col + 1 < cols and game_board[row][center_col + 1] == side:
            score += weight.adj_col_merit

    return score


# This function adds two arrays element-wise
def add_arrays(arr1, arr2):
    return [arr1[i] + arr2[i] for i in range(len(arr1))]


# This function calculates how close the player is to winning
# in the horizontal direction
def horizontal_weight(game_board, side):
    rows = len(game_board)
    cols = len(game_board[0])
    total_array = [0, 0, 0, 0]

    for row in range(rows):
        # minus 3 to ensure the calculation is within the board limits
        for col in range(cols - 3):
            window = [game_board[row][col + i] for i in range(4)]
            total_array = add_arrays(total_array, window_calculation(window, side))

    return total_array


# This function calculates how close the player is to winning
# in the vertical direction
def vertical_weight(game_board, side):
    rows = len(game_board)
    cols = len(game_board[0])
    total_array = [0, 0, 0, 0]

    for col in range(cols):
        # minus 3 to ensure the calculation is within the board limits
        for row in range(rows - 3):
            window = [game_board[row + i][col] for i in range(4)]
            total_array = add_arrays(total_array, window_calculation(window, side))

    return total_array


# This function calculates how close the player is to winning
# in the diagonal direction (top-left to bottom-right)
def diagonal_weight_l(game_board, side):
    rows = len(game_board)
    cols = len(game_board[0])
    total_array = [0, 0, 0, 0]

    # minus 3 to ensure the calculation is within the board limits
    for row in range(rows - 3):
        for col in range(cols - 3):
            window = [game_board[row + i][col + i] for i in range(4)]
            total_array = add_arrays(total_array, window_calculation(window, side))

    return total_array


# This function calculates how close the player is to winning
# in the diagonal direction (bottom-left to top-right)
def diagonal_weight_r(game_board, side):
    rows = len(game_board)
    cols = len(game_board[0])
    total_array = [0, 0, 0, 0]

    # minus 3 to ensure the calculation is within the board limits
    for row in range(3, rows):
        for col in range(cols - 3):
            window = [game_board[row - i][col + i] for i in range(4)]
            total_array = add_arrays(total_array, window_calculation(window, side))

    return total_array


# This function add weight according to how close the window is to winning
# A window is a sub-section of the game board of 4 adjacent cells
def window_calculation(window, side):
    opponent = 1 if side == 2 else 2

    # Count player piece, opponent piece, and empty spaces in the window
    player_pieces = window.count(side)
    opponent_pieces = window.count(opponent)
    empty_spaces = window.count(0)

    # Initialize the array to store the number of match cases
    # [4-piece, 3-piece, 2-piece, opponent 3-piece]
    result = [0, 0, 0, 0]  

    # 4 piece in a row: Winning move
    if player_pieces == 4: 
        result[0] += 1

    # 3 piece in a row & 1 empty cell: 1 move away from winning
    elif player_pieces == 3 and empty_spaces == 1:
        result[1] += 1
        
    # 2 piece in a row & 2 empty cell: 2 move away from winning
    elif player_pieces == 2 and empty_spaces == 2: 
        result[2] += 1

    # 3 oppenent piece in a row & 1 empty cell: 1 move away from losing
    elif opponent_pieces == 3 and empty_spaces == 1: 
        result[3] += 1

    return result


# This function perform minimax algorithm to find the score for placing piece at each column
def minimax_move(game_board, side, depth, minimax_tree):
    cols = len(game_board[0])

    # Determine the opponent's side
    opponent = 1 if side == 2 else 2  

    # Initialize scores for each column
    scores = [-math.inf] * cols  

    # Calculate the score for each column
    for col in range(cols):
        if not column_avail(game_board, col):
            # Column is not available
            scores[col] = "NA"  
            continue

        next_board = clone_and_place_piece(game_board, side, col)

        alpha = -math.inf
        beta = math.inf

        # Calculate the score for placing in this column using minimax with alpha-beta pruning
        scores[col] = minimax(next_board, depth - 1, alpha, beta, False, side, opponent, minimax_tree, 0, col)

    return scores


# This function checks if a column is available to place piece, i.e. not full
def column_avail(game_board, column):
    if game_board[0][column] == 0: return True
    return False


# This function returns the available columns to place a piece
def columns_avail(game_board):
    cols = len(game_board[0])
    valid_columns = [col for col in range(cols) if column_avail(game_board, col)]

    if DEBUG_2: print(f"Valid columns: {valid_columns}")

    return valid_columns


# This function simulates placing a piece in the game board at a specific column
def clone_and_place_piece(board, side, column):
    new_board = [row[:] for row in board]  # Deep copy of the board

    for row in reversed(range(len(board))):  # Start from the bottom row
        if new_board[row][column] == 0:
            new_board[row][column] = side
            if DEBUG_2: print(f"Placed piece for side {side} in column {column}, row {row}")
            return new_board
        
    if DEBUG_2: print(f"Column {column} is full, cannot place piece for side {side}")

    return new_board


def minimax(board, depth, alpha, beta, maximizing_player, side, opponent, minimax_tree, current_depth=0, current_col=None):
    valid_columns = columns_avail(board)
    is_terminal = check_win(board, side) or check_win(board, opponent) or len(valid_columns) == 0

    if DEBUG_2:
        print(f"Depth: {depth}, Valid Columns: {valid_columns}, Current Column: {current_col}")

    # Generate the key for the current node
    current_key = f"depth_{current_depth}_col_{current_col}" if current_col is not None else f"depth_{current_depth}"

    # Initialize the current node in the tree if not already present
    if current_key not in minimax_tree:
        minimax_tree[current_key] = {"score": None, "children": {}}

    # Base case: terminal state or depth reached
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, side):  # Maximizing player wins
                score = math.inf
            elif check_win(board, opponent):  # Opponent wins
                score = -math.inf
            else:  # Draw
                score = 0
        else:
            score = evaluation(board, side)

        # Store the score in the tree
        minimax_tree[current_key]["score"] = score
        return score

    if maximizing_player:
        max_eval = -math.inf

        for col in valid_columns:
            next_board = clone_and_place_piece(board, side, col)
            subtree_key = f"depth_{current_depth + 1}_col_{col}"

            # Ensure the subtree is initialized
            if subtree_key not in minimax_tree[current_key]["children"]:
                minimax_tree[current_key]["children"][subtree_key] = {"score": None, "children": {}}

            eval = minimax(next_board, depth - 1, alpha, beta, False, side, opponent, minimax_tree[current_key]["children"], current_depth + 1, col)

            if DEBUG_2: print(f"Evaluating column {col}, depth {current_depth}, score {eval}, max_score {max_eval}, alpha {alpha}, beta {beta}")

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            # Record the score of the node that triggered pruning
            minimax_tree[current_key]["children"][subtree_key]["score"] = eval

            if beta <= alpha:
                if DEBUG_2: print(f"Pruning at column {col}, depth {current_depth}")

                # Mark remaining nodes as "x"
                for remaining_col in valid_columns[valid_columns.index(col) + 1:]:
                    pruned_key = f"depth_{current_depth + 1}_col_{remaining_col}"
                    minimax_tree[current_key]["children"][pruned_key] = {"score": "x", "children": {}}
                break

        minimax_tree[current_key]["score"] = max_eval
        return max_eval
    else:
        min_eval = math.inf

        for col in valid_columns:
            next_board = clone_and_place_piece(board, opponent, col)
            subtree_key = f"depth_{current_depth + 1}_col_{col}"

            # Ensure the subtree is initialized
            if subtree_key not in minimax_tree[current_key]["children"]:
                minimax_tree[current_key]["children"][subtree_key] = {"score": None, "children": {}}

            eval = minimax(next_board, depth - 1, alpha, beta, True, side, opponent, minimax_tree[current_key]["children"], current_depth + 1, col)
            
            if DEBUG_2: print(f"Evaluating column {col}, depth {current_depth}, score {eval}, min_score {min_eval}, alpha {alpha}, beta {beta}")
            
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            # Record the score of the node that triggered pruning
            minimax_tree[current_key]["children"][subtree_key]["score"] = eval

            if beta <= alpha:
                if DEBUG_2: print(f"Pruning at column {col}, depth {current_depth}")

                # Mark remaining nodes as "x"
                for remaining_col in valid_columns[valid_columns.index(col) + 1:]:
                    pruned_key = f"depth_{current_depth + 1}_col_{remaining_col}"
                    minimax_tree[current_key]["children"][pruned_key] = {"score": "x", "children": {}}
                break

        minimax_tree[current_key]["score"] = min_eval
        return min_eval