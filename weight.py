# this file is the parameters for the weight used in score evaluation

### center row preference ###

# occupying the center col
center_col_merit = 10

# occupying the column adjacent to the center col
adj_col_merit = 5


### 4-cell window evaluation ###
 
# 4-piece: Winning move
# Highest priority, guarantees a win
winning_move_4p = 1000000

# 3-piece: 1 move away from winning
# Single 3-piece-in-a-row, important for progress
winning_move_3p = 300000

# 2-piece: 2 moves away from winning
# Single 2-piece-in-a-row, lowest priority
winning_move_2p = 100000

# 3 opponent piece: 1 move away from losing
# Second highest priority, prevents losing
losing_move_3p = 900000


### multiple winning pattern bonus ###

# 2 or more 4-piece: Winning move
# Multiple 4-piece-in-a-row, still guarantees a win
m_winning_move_4p = 800000

# 2 or more 3-piece: 1 move away from winning
# Multiple 3-piece-in-a-row, very close to winning
m_winning_move_3p = 500000

# 2 or more 2-piece: 2 moves away from winning
# Multiple 2-piece-in-a-row, still important
m_winning_move_2p = 10000