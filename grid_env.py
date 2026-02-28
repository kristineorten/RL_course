
import numpy as np
import constants as const
from cell import Cell  

class GridEnv():
    """
    GridEnv example:
        Size 2x3 means width = 2 and length = 3, or 2 rows, 3 columns.
        Coordinates are indexed in order (row, col):
            (x  , y) (x  , y+1) (x  , y+2)
            (x+1, y) (x+1, y+1) (x+1, y+2)
        (0, 0) is the top left corner, (width-1, length-1) is the bottom right corner.

    """
    def __init__(self, width, length, start_x, start_y, end_x, end_y, verbose=False):
        self.verbose = verbose
        if self.verbose:
            print("Initializing Grid Environment...")
        
        assert 0 <= start_y < length and 0 <= start_x < width, "Starting position out of bounds"
        assert 0 <= end_y < length and 0 <= end_x < width, "Ending position out of bounds"

        self.num_cols = length
        self.num_rows = width
        self.start_pos = Cell(start_x, start_y)
        self.end_pos = Cell(end_x, end_y)
        self.curr_pos = self.start_pos
        
        self.terminated = False
        
        self.world = np.zeros((self.num_rows, self.num_cols))
        self.world[start_x, start_y] = const.START
        self.world[end_x, end_y] = const.GOAL

        if self.verbose:
            print(f"Initialized Grid Environment of size {width}x{length} with start at ({start_x},{start_y}) and goal at ({end_x},{end_y})")        

    ### Setup functions ###
    def add_wall(self, x, y):
        assert 0 <= x < self.num_rows and 0 <= y < self.num_cols, "Wall position out of bounds"
        assert self.world[x, y] == const.EMPTY, "Can only place wall on an empty cell"

        self.world[x, y] = const.WALL
        
        if self.verbose:
            print(f"Added wall at position ({x},{y})")
        
    def add_trap(self, x, y):
        assert 0 <= x < self.num_rows and 0 <= y < self.num_cols, "Trap position out of bounds"
        assert self.world[x, y] == const.EMPTY, "Can only place trap on an empty cell"
        
        self.world[x, y] = const.TRAP
        
        if self.verbose:
            print(f"Added trap at position ({x},{y})")
        
    ### Gameplay functions ###
    def reset(self) -> tuple[Cell, int, bool, list]:
        """
        Reset the environment to the starting state.

        Parameters:
            None
        
        Returns:
            current position (Cell)
            reward (int)
            termination status (bool)
            info (list)
        """
        self.terminated = False
        self.curr_pos = self.start_pos

        if self.verbose:
            print("Environment reset to starting position.")
        
        return self.curr_pos, 0, self.terminated, []
    
    def step(self, action) -> tuple[Cell, int, bool, list]:
        """
        Perform chosen action in the environment.

        Parameters:
            action (int): The action taken by the agent, either const.UP, const.DOWN, const.LEFT, or const.RIGHT
        
        Returns:
            current position (Cell)
            reward (int)
            termination status (bool)
            info (list): List of messages regarding the transition, reward, and termination status for debugging purposes.
        """
        
        if (not self.terminated):
            self.curr_pos, transition_msgs = self._compute_transition(action)
            reward, reward_msgs = self._compute_reward()
            terminated_msgs = self._check_termination()

            if self.verbose:
                print(f"Action taken: {action}, New position: {self.curr_pos}, Reward: {reward}, Terminated: {self.terminated}")

            return self.curr_pos, reward, self.terminated, [transition_msgs, reward_msgs, terminated_msgs]
        
        else:
            if self.verbose:
                print("Attempted a step in a terminated environment.")
            return Cell(-1,-1), -1, self.terminated, ["No action taken", "No reward computed", "Game already finished"]
        
    def _compute_transition(self, action) -> tuple[Cell, str]:
        """
        Get the next position based on the action taken.

        Parameters:
            action (int): The action taken by the agent, either const.UP, const.DOWN, const.LEFT, or const.RIGHT

        Returns:
            new position (Cell)
            transition message (str)
        """
        if self.verbose: print("Computing transition.")

        row = self.curr_pos.row
        col = self.curr_pos.col
        new_row = row
        new_col = col

        action_text = ""
        if action == const.UP:
            new_row = row - 1
            action_text = "UP"
            if self.verbose: print("Action UP chosen.")
        elif action == const.DOWN:
            new_row = row + 1
            action_text = "DOWN"
            if self.verbose: print("Action DOWN chosen.")
        elif action == const.LEFT:
            new_col = col - 1
            action_text = "LEFT"
            if self.verbose: print("Action LEFT chosen.")
        elif action == const.RIGHT:
            new_col = col + 1
            action_text = "RIGHT"
            if self.verbose: print("Action RIGHT chosen.")

        if (new_row < 0 or new_row >= self.num_rows or new_col < 0 or new_col >= self.num_cols): 
            # Move out of bounds
            return self.curr_pos, "I can not move out of the world"
        elif (self.world[new_row, new_col] == const.WALL): 
            # Move into a wall
            return self.curr_pos, "I can not move through a wall"
        else: 
            # Move accepted
            # Note: Moves into traps or goals are allowed, termination and reward will be handled separately
            return Cell(new_row, new_col), f"I moved {action_text}"
        
    def _compute_reward(self) -> tuple[int, str]:
        """
        Calculate the received reward based on the new position.
        Default reward for each step is -1, to encourage shorter paths.
        Reaching the goal gives a reward of 100 and falling into a trap gives a reward of -100.

        Input:
            None

        Returns:
            reward (int)
            reward message (str)
        """

        reward = -1
        if (self.curr_pos == self.end_pos):
            # Goal has been reached
            reward = 100
        elif (self.world[self.curr_pos.row, self.curr_pos.col] == const.TRAP):
            # Agent has fallen into a trap
            reward = -100 
        return reward, "Reward computed"
        
    def _check_termination(self) -> str:
        """
        Game terminates if agent reaches the goal or falls into a trap.
        Termination message is empty, if the game is not terminated, otherwise it gives the reason for termination.

        Parameters:
            None    

        Returns:
            Termination message (str)
        """

        termination_msg = ""

        if (self.curr_pos == self.end_pos):
            self.terminated = True
            termination_msg = "I reached the goal!"

        elif (self.world[self.curr_pos.row, self.curr_pos.col] == const.TRAP):
            self.terminated = True
            termination_msg = "I fell into a trap!"

        return termination_msg
    
    ### Print functions ###
    def _get_env_representation(self):
        env_copy = self.world.copy()
        env_copy[self.curr_pos.row, self.curr_pos.col] = const.PLAYER
        return env_copy
                
    def print_basic(self):
        np.set_printoptions(formatter={"float": " {: 0.0f} ".format})
        
        env_printable = self._get_env_representation()
        print(env_printable)
        print("\n")
  
        np.set_printoptions()
        
    def print_unicode(self):
        env_printable = self._get_env_representation()
        
        rows = []
        for i in range(self.num_rows):
            rows.append([const.cell_value_to_unicode(int(env_printable[i,j])) for j in range(self.num_cols)])
        for i in range(self.num_rows):
            print(*rows[i], sep=" ")
        print("\n")
    
        