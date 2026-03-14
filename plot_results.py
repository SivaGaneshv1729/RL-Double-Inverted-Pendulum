import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_results():
    log_dirs = ["logs/baseline", "logs/shaped"]
    plt.figure(figsize=(10, 6))

    for log_dir in log_dirs:
        if not os.path.exists(log_dir):
            print(f"Directory {log_dir} not found. Skipping.")
            continue
            
        # Find the monitor file
        files = [f for f in os.listdir(log_dir) if f.endswith("monitor.csv")]
        if not files:
            print(f"No monitor file found in {log_dir}. Skipping.")
            continue
            
        file_path = os.path.join(log_dir, files[0])
        
        # SB3 monitor files have 2 header lines
        df = pd.read_csv(file_path, skiprows=1)
        
        # Calculate rolling mean for smoother plot
        df['r_rolling'] = df['r'].rolling(window=10).mean()
        
        # 't' is time, 'r' is reward, 'l' is length
        # Cumulative timesteps
        df['timesteps'] = df['l'].cumsum()
        
        reward_type = log_dir.split("/")[-1]
        plt.plot(df['timesteps'], df['r_rolling'], label=f"{reward_type.capitalize()} Reward")

    plt.title("Double Inverted Pendulum: Training Comparison")
    plt.xlabel("Timesteps")
    plt.ylabel("Mean Reward (10-ep Rolling)")
    plt.legend()
    plt.grid(True)
    plt.savefig("reward_comparison.png")
    print("Plot saved as reward_comparison.png")
    # plt.show()

if __name__ == "__main__":
    plot_results()
