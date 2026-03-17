import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from environment import DoublePendulumEnv

def train():
    parser = argparse.ArgumentParser(description="Train PPO agent for Double Inverted Pendulum")
    parser.add_argument("--timesteps", type=int, default=200000, help="Total training timesteps")
    parser.add_argument("--reward_type", type=str, default="shaped", choices=["baseline", "shaped"], help="Reward function type")
    parser.add_argument("--save_path", type=str, default="models/ppo_double_pendulum", help="Path to save the model")
    args = parser.parse_args()

    # Create directories
    os.makedirs("models", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    log_dir = f"logs/{args.reward_type}"
    os.makedirs(log_dir, exist_ok=True)

    # Initialize environment
    env = DoublePendulumEnv(reward_type=args.reward_type)
    
    # Check if environment follows gym API
    print("Checking environment...")
    check_env(env)
    
    # Wrap environment for logging
    env = Monitor(env, log_dir)

    # Instantiate PPO agent
    print(f"Instantiating PPO agent with {args.reward_type} reward (Iteration 5)...")
    
    policy_kwargs = dict(
        net_arch=[256, 256], # Larger network for chaotic dynamics
    )
    
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=5e-5, # Slightly faster for Iteration 6 authority
        n_steps=32768,      # Maintain large window
        batch_size=512,     
        n_epochs=10,
        gamma=0.999,        
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        policy_kwargs=policy_kwargs,
    )

    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=100000,
        save_path="./models/",
        name_prefix=f"ppo_double_pendulum_{args.reward_type}_checkpoint"
    )

    # Train the agent
    print(f"Starting training for {args.timesteps} timesteps...")
    model.learn(total_timesteps=args.timesteps, callback=checkpoint_callback)

    # Save the model
    final_save_path = f"{args.save_path}_{args.reward_type}"
    model.save(final_save_path)
    print(f"Model saved to {final_save_path}.zip")

    env.close()

if __name__ == "__main__":
    train()
