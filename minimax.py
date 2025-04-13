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