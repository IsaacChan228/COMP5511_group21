# this file is the parameters for the weight used in score evaluation

### center row preference ###

# occupying the center col
center_col_merit = 5

# occupying the column adjacent to the center col
adj_col_merit = 3


### 4-cell window evaluation ###
 
# 4-piece: Winning move
# Highest priority, guarantees a win
winning_move_4p = 10000

# 3-piece: 1 move away from winning
# Single 3-piece-in-a-row, important for progress
winning_move_3p = 500

# 2-piece: 2 moves away from winning
# Single 2-piece-in-a-row, lowest priority
winning_move_2p = 100

# 3 opponent piece: 1 move away from losing
# Second highest priority, prevents losing
losing_move_3p = -8000


### multiple winning pattern bonus ###

# 2 or more 3-piece: 1 move away from winning
# Multiple 3-piece-in-a-row, very close to winning
# This do not check if the multiple 3-piece-in-a-row two-ended, which is a winning move
m_winning_move_3p = 4000

# 2 or more 2-piece: 2 moves away from winning
# Multiple 2-piece-in-a-row, still important
m_winning_move_2p = 500

# 2 or more 3 opponent piece: 1 move away from losing
# Multiple 3 opponent piece-in-a-row, very close to losing
m_losing_move_3p = -6000


### 2-sided 2-piece-in-a-row bonus ###
# 2-sided 2-piece-in-a-row
# better than 1-sided 2-piece-in-a-row
m_2sided_2pp = 200

# 2-sided 2 opponent piece-in-a-row
# worse than 1-sided 2-opponent piece-in-a-row
m_2sided_2op = -200