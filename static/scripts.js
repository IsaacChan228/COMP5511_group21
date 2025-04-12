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
        const gameBoard = data.game_board;

        // Update the cells based on the new game board values
        document.querySelectorAll('.cell').forEach(cell => {
            const row = parseInt(cell.getAttribute('data-row'));
            const col = parseInt(cell.getAttribute('data-col'));
            const value = gameBoard[row][col];

            // Reset the cell's class
            cell.className = 'cell';

            // Apply the appropriate class based on the value
            if (value === 1) {
                cell.classList.add('red');
            } else if (value === 2) {
                cell.classList.add('green');
            }
        });
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
            updateGameBoard();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

// When "Verify State" button is clicked, send a request to verify the current game state
document.getElementById('verify-state-button').addEventListener('click', () => {
    fetch('/verify-state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // Display the result in the state-result div
        const resultDiv = document.getElementById('state-result');
        resultDiv.textContent = data.message; // Set the result message
        resultDiv.style.display = 'block'; // Ensure the div is visible
    })
    .catch(error => {
        console.error('Error verifying state:', error);
    });
});

// When "Clear Message" button is clicked, hide the state-result message
document.getElementById('clear-message-button').addEventListener('click', () => {
    const resultDiv = document.getElementById('state-result');
    resultDiv.style.display = 'none'; // Hide the state-result div
    resultDiv.textContent = ''; // Clear the message content
});

// When "Reset Game Board" button is clicked, send a request to reset the game board
document.getElementById('reset-board-button').addEventListener('click', () => {
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

        // Hide the state-result message
        const resultDiv = document.getElementById('state-result');
        resultDiv.style.display = 'none'; // Hide the state-result div
        resultDiv.textContent = ''; // Clear the message content

    })
    .catch(error => {
        console.error('Error resetting game board:', error);
    });
});

