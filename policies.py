
import numpy as np
import constants as const

def policy_random(state):
    """Random action regardless of environment state."""
    return int(np.random.choice(const.actions))

def policy1(state):
    if (state.row == 3):
        return const.RIGHT
    else:
        return const.DOWN
    
def policy2(state):
    """
    Move as a snake from start A (0,0) to goal G (3,3):
    A   > > v
    v   ^   v
    v   ^   v
    > > ^   G
    Other positions move RIGHT.
    """
    if (state.col == 0) & (state.row < 3):
        return const.DOWN
    elif (state.col == 2) & (state.row > 0):
        return const.UP
    elif (state.col == 4) & (state.row < 3):
        return const.DOWN
    else:
        return const.RIGHT

def policy1_epsilon(state, eps = 0.2):
    if (np.random.random() < eps):
        return policy_random(state)
    else:
        return policy1(state)
