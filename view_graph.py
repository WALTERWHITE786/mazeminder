# view_graph.py
import matplotlib.pyplot as plt
import numpy as np

REWARDS_FILE = 'rewards.npy'

try:
    # Load the saved rewards data
    rewards = np.load(REWARDS_FILE)

    print("Generating graph from saved rewards data...")

    # Plotting logic (copied from train.py)
    plt.figure(figsize=(12, 6))
    plt.plot(np.convolve(rewards, np.ones(100)/100, mode='valid'))
    plt.title("Guardian's Learning Progress (Moving Average)")
    plt.xlabel("Episode")
    plt.ylabel("Average Reward")
    plt.grid(True)
    
    # Save the figure and show it
    plt.savefig('training_rewards.png')
    print("Graph saved as 'training_rewards.png'")
    plt.show()

except FileNotFoundError:
    print(f"Error: Could not find '{REWARDS_FILE}'.")
    print("Please run the training script (python -m src.train) first.")