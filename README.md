# COMP5511_group21

Members: 
CHAN Lok Hay (24014193G)
Siu Po TAI
Lok Him Rhine WOO
Ming Sum YAU


Scope to be discussed:
1. We can either do an evalutor, such that the user provide a game state, and the AI gen the score for each next move, or
2. like the examples, create an interactive game, such that the user play with the AI, or
3. both if we have time

Please share your comment


Things to be done:
1. find and implement a interactive GUI that can actively sync the game state array with backend code
2. Build the basic layout of the GUI
3. Add the function that check the winning moves/ winning state
4. Add the function that evaluate the score of each move
    - give a very high score to winning moves
    - give a very high penalty if opponent next move will win the game, etc.
5. Add and customize the MinimaxTree to the code, with debug function to display the min/max values for report


13 Apr update by Isaac:
- evaluator version with html GUI and flask handler is created
- minimax tree implemented
- may need tuning on the weight of each state, but can do it later
- minimax tree is exported to minimax_tree.JSON

- How to run the code
    1. pip install -r requirement.txt
    2. python connect4.py
    3. a flask utility should be running at (http://127.0.0.1:5000)
    4. remember to ctrl+C to stop the utility when done