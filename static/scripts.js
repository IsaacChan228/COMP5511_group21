// Update the game board per the backend response
function updateGameBoard() {
    fetch('/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the response from the backend

        const gameBoard = data.game_board;
        const nextMove = data.next_move;

        // Update the cells based on the new game board values
        updateGameBoardCells(gameBoard);

        // Update the "Next Move" cell
        updateNextMove(nextMove);
    })
    .catch(error => {
        console.error('Error updating game board:', error);
    });
}


// When game board cell is clicked, send the updated state of the game board to the backend
document.querySelectorAll('.cell').forEach(cell => {
    cell.addEventListener('click', () => {
        const row = cell.getAttribute('data-row');
        const col = cell.getAttribute('data-col');

        // Send the row and column to the backend
        fetch('/cell-click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ row: parseInt(row), col: parseInt(col) }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Log the response from the backend
            updateGameBoard(); // Refresh the game board
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


// When "Invert State" button is clicked, send a request to verify the current game state
document.getElementById('invert-state-button').addEventListener('click', () => {
    clearScoresFromCells(); // Clear scores
    fetch('/invert-state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the response from the backend

        updateGameBoard(); // Refresh the game board on the frontend
    })
    .catch(error => {
        console.error('Error inverting state:', error);
    });
});


// When "Verify State" button is clicked, send a request to verify the current game state
document.getElementById('verify-state-button').addEventListener('click', () => {
    clearScoresFromCells(); // Clear scores
    fetch('/verify-state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the response from the backend

        // Display the result in the state-result div
        const stateResultDiv = document.getElementById('state-result');
        const minimaxDiv = document.getElementById('minimax-result');

        stateResultDiv.textContent = data.message; // Set the result message
        stateResultDiv.style.display = 'block'; // Ensure the div is visible
        minimaxDiv.style.display = 'none'; // Hide the minimax-result div
    })
    .catch(error => {
        console.error('Error verifying state:', error);
    });
});


// When "Clear Message" button is clicked, clear both state-result and minimax-result messages
document.getElementById('clear-message-button').addEventListener('click', () => {
    clearScoresFromCells(); // Clear scores
    const stateResultDiv = document.getElementById('state-result');
    const minimaxResultDiv = document.getElementById('minimax-result');

    // Hide both divs and clear their content
    stateResultDiv.style.display = 'none';
    stateResultDiv.textContent = '';
    minimaxResultDiv.style.display = 'none';
    minimaxResultDiv.textContent = '';
});


// When "Reset Game Board" button is clicked, send a request to reset the game board
document.getElementById('reset-board-button').addEventListener('click', () => {
    clearScoresFromCells(); // Clear scores
    fetch('/reset-board', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the response from the backend

        updateGameBoard(); // Refresh the game board on the frontend

        // Hide both state-result and minimax-result divs
        const stateResultDiv = document.getElementById('state-result');
        const minimaxResultDiv = document.getElementById('minimax-result');

        stateResultDiv.style.display = 'none';
        stateResultDiv.textContent = '';
        minimaxResultDiv.style.display = 'none';
        minimaxResultDiv.textContent = '';
    })
    .catch(error => {
        console.error('Error resetting game board:', error);
    });
});


// When "Next Move" cell is clicked, send a request to the backend
document.getElementById('next-move').addEventListener('click', () => {
    fetch('/nextmove-click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the response from the backend

        updateNextMove(data.next_move); // Pass the updated value from the backend
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


// Function to update the color of the "Next Move" cell
function updateNextMove(value) {
    const nextMove = document.getElementById('next-move');

    // Reset the cell's class
    nextMove.className = 'next-move';

    // Apply the appropriate class based on the value
    if (value === 1) {
        nextMove.classList.add('red'); // Red for player 1
    } else if (value === 2) {
        nextMove.classList.add('green'); // Green for player 2
    }
     else {
        console.warn('Invalid next_move value:', value);
    }
}


// Function to update the color of the cells of the game board
function updateGameBoardCells(gameBoard) {
    document.querySelectorAll('.cell').forEach(cell => {
        const row = parseInt(cell.getAttribute('data-row'));
        const col = parseInt(cell.getAttribute('data-col'));
        const value = gameBoard[row][col];

        // Reset the cell's class
        cell.className = 'cell';

        // Apply the appropriate class based on the value
        if (value === 1) {
            cell.classList.add('red'); // Red for player 1
        } else if (value === 2) {
            cell.classList.add('green'); // Green for player 2
        }
    });
}


// When "Minimax" button is clicked, calculate the score for each column
document.getElementById('minimax-button').addEventListener('click', () => {
    clearScoresFromCells(); // Clear scores
    fetch('/minimax', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the response from the backend
        console.log('Minimax scores:', data.scores); // Log the scores

        const stateResultDiv = document.getElementById('state-result');
        const resultDiv = document.getElementById('minimax-result');

        if (data.scores.length === 0) {
            // If scores are empty, display the error message
            stateResultDiv.textContent = data.message;
            stateResultDiv.style.display = 'block'; // Ensure the div is visible
            resultDiv.style.display = 'none'; // Hide the minimax-result div
        } else {
            // Otherwise, display the scores
            resultDiv.textContent = `Scores for each column: ${data.scores.join(', ')}`;
            resultDiv.style.display = 'block'; // Ensure the div is visible
            stateResultDiv.style.display = 'none'; // Hide the state-result div

            // Place the scores in the corresponding cells
            placeScoresInCells(data.scores);
        }
    })
    .catch(error => {
        console.error('Error calculating minimax:', error);
    });
});


// Function to place scores on top of the lowest unoccupied cell (white cell)
function placeScoresInCells(scores) {
    const rows = 6; // Number of rows in the game board
    const cols = 7; // Number of columns in the game board

    for (let col = 0; col < cols; col++) {
        const score = scores[col];

        // Skip if the score is "NA"
        if (score === "NA") continue;

        // Find the lowest unoccupied cell in the column
        for (let row = rows - 1; row >= 0; row--) {
            const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
            if (cell && !cell.classList.contains('red') && !cell.classList.contains('green')) {
                // Create a non-interactive overlay for the score
                const scoreOverlay = document.createElement('div');
                scoreOverlay.textContent = score; // Set the score text
                scoreOverlay.classList.add('score-overlay'); // Add a class for styling
                scoreOverlay.style.pointerEvents = 'none'; // Make it non-interactive

                // Position the overlay on top of the cell
                cell.style.position = 'relative'; // Ensure the cell is positioned relative
                scoreOverlay.style.position = 'absolute';
                scoreOverlay.style.top = '0';
                scoreOverlay.style.left = '0';
                scoreOverlay.style.width = '100%';
                scoreOverlay.style.height = '100%';
                scoreOverlay.style.display = 'flex';
                scoreOverlay.style.justifyContent = 'center';
                scoreOverlay.style.alignItems = 'center';
                scoreOverlay.style.color = 'blue'; // Set the text color
                scoreOverlay.style.fontWeight = 'bold';

                // Append the overlay to the cell
                cell.appendChild(scoreOverlay);
                break;
            }
        }
    }
}

// Function to clear scores from all cells
function clearScoresFromCells() {
    document.querySelectorAll('.cell').forEach(cell => {
        const scoreOverlay = cell.querySelector('.score-overlay');
        if (scoreOverlay) {
            scoreOverlay.remove(); // Remove the score overlay
        }
    });
}