# src/train.py
"""
Training script for the MazeMinderAgent.
Runs a non-graphical simulation to train the Q-Learning agent.
"""
import numpy as np
import matplotlib.pyplot as plt
import random
# Use relative imports
from .agent import MazeMinderAgent
from .settings import *

class SimulatedPlayer:
    """Simulates a player with a defined skill level."""
    def __init__(self, skill=0.5):
        self.skill = skill

    def play(self, difficulty, has_key_objective):
        """Simulates playing a level."""
        total_difficulty = difficulty + (0.2 if has_key_objective else 0)
        performance = self.skill - total_difficulty + np.random.uniform(-0.1, 0.1)
        self.skill = min(1.0, self.skill + 0.005)
        return max(0.0, min(1.0, performance))

def get_state(performance):
    """Discretizes a performance score into one of three states."""
    if performance < 0.33: return 0  # Struggling
    if performance < 0.66: return 1  # Learning
    return 2  # Mastery

def get_reward(prev_state, new_state):
    """Calculates reward based on the transition between states."""
    if prev_state == 0 and new_state == 1: return 20  # Struggling -> Learning (Best outcome)
    if prev_state == 1 and new_state == 2: return 10  # Learning -> Mastery (Good progress)
    if prev_state == 1 and new_state == 1: return 5   # Stay in Learning (Optimal zone)
    if prev_state == 2 and new_state == 1: return -10 # Too hard, frustrated expert
    if prev_state == 1 and new_state == 0: return -20 # Way too hard, major penalty
    if new_state == 0: return -5 # Penalty for being in struggling state
    if prev_state == 2 and new_state == 2: return -2 # Small penalty for boredom
    return 0

def train():
    """Executes the main training loop for the agent."""
    agent = MazeMinderAgent()
    agent.epsilon = EPSILON_START
    rewards = []
    print("--- Training the Archive Guardian ---")
    
    for episode in range(NUM_EPISODES):
        # Initialize a new player with random skill for diversity
        player = SimulatedPlayer(np.random.uniform(0.2, 0.6))
        state = get_state(player.play(0, False)) # Initial performance
        episode_reward = 0

        for _ in range(MAX_STEPS_PER_EPISODE):
            action = agent.choose_action(state)
            
            # Map action (0-3) to difficulty (0.0-1.0)
            action_difficulty = action / (NUM_ACTIONS - 1)
            # Randomly decide if this level will have a key objective
            has_key = random.random() < 0.5 
            
            performance = player.play(action_difficulty, has_key)
            next_state = get_state(performance)
            reward = get_reward(state, next_state)
            
            agent.learn(state, action, reward, next_state)
            state = next_state
            episode_reward += reward
        
        # Epsilon decay
        if agent.epsilon > EPSILON_MIN:
            agent.epsilon *= EPSILON_DECAY

        rewards.append(episode_reward)
        if (episode + 1) % 500 == 0:
            avg_reward = np.mean(rewards[-500:])
            print(f"Episode {episode + 1}/{NUM_EPISODES} | Avg Reward: {avg_reward:.2f} | Epsilon: {agent.epsilon:.3f}")

    print("--- Training Complete ---")
    agent.save_q_table()
    
    # Save reward data and plot
    np.save('rewards.npy', rewards)
    
    plt.figure(figsize=(12, 6))
    plt.plot(np.convolve(rewards, np.ones(100)/100, mode='valid'))
    plt.title("Guardian's Learning Progress (Moving Average)")
    plt.xlabel("Episode")
    plt.ylabel("Average Reward")
    plt.grid(True)
    plt.savefig('training_rewards.png')
    plt.show()

if __name__ == '__main__':
    train()