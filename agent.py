# src/agent.py
"""
Contains the MazeMinderAgent class, which implements the Q-Learning algorithm.
The agent learns a policy to select maze transformations to optimize player learning.
"""
import numpy as np
import pickle
# Use relative import
from .settings import NUM_STATES, NUM_ACTIONS, ALPHA, GAMMA, EPSILON_START, Q_TABLE_PATH

class MazeMinderAgent:
    """
    A Q-Learning agent that learns to select maze transformations.
    """
    def __init__(self, load_q_table=False):
        """Initializes the agent."""
        if load_q_table:
            self.q_table = self._load_q_table()
            self.epsilon = 0 # No exploration if pre-trained
        else:
            self.q_table = np.zeros((NUM_STATES, NUM_ACTIONS))
            self.epsilon = EPSILON_START 
        
        self.alpha = ALPHA
        self.gamma = GAMMA

    def choose_action(self, state):
        """Chooses an action using an epsilon-greedy policy."""
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(NUM_ACTIONS)  # Explore
        else:
            return np.argmax(self.q_table[state, :])  # Exploit

    def learn(self, state, action, reward, next_state):
        """Updates the Q-table using the Bellman equation."""
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state, :])
        
        # Bellman equation
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[state, action] = new_value

    def save_q_table(self, path=Q_TABLE_PATH):
        """Saves the current Q-table to a file using pickle."""
        try:
            with open(path, 'wb') as f:
                pickle.dump(self.q_table, f)
            print(f"Q-table successfully saved to {path}")
        except Exception as e:
            print(f"Error saving Q-table: {e}")

    def _load_q_table(self, path=Q_TABLE_PATH):
        """Loads a Q-table from a file."""
        try:
            with open(path, 'rb') as f:
                q_table = pickle.load(f)
            print(f"Q-table loaded from {path}")
            return q_table
        except FileNotFoundError:
            print(f"Warning: No Q-table found at {path}. Initializing a new one.")
            return np.zeros((NUM_STATES, NUM_ACTIONS))
        except Exception as e:
            print(f"Error loading Q-table: {e}. Initializing a new one.")
            return np.zeros((NUM_STATES, NUM_ACTIONS))