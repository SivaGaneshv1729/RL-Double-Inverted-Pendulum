import os
import argparse
import imageio
import numpy as np
from stable_baselines3 import PPO
from environment import DoublePendulumEnv

def evaluate():
    parser = argparse.ArgumentParser(description="Evaluate PPO agent for Double Inverted Pendulum")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the saved model .zip file")
    parser.add_argument("--episodes", type=int, default=5, help="Number of episodes to run")
    parser.add_argument("--gif_name", type=str, default=None, help="If provided, save a GIF of the evaluation")
    parser.add_argument("--steps", type=int, default=1000, help="Maximum steps per episode")
    args = parser.parse_args()

    # Create media directory if saving GIF
    if args.gif_name:
        os.makedirs("media", exist_ok=True)

    # Initialize environment
    env = DoublePendulumEnv(render_mode="human" if not args.gif_name else "rgb_array")
    
    # Load model
    print(f"Loading model from {args.model_path}...")
    model = PPO.load(args.model_path, env=env)

    frames = []

    for ep in range(args.episodes):
        obs, info = env.reset()
        done = False
        truncated = False
        score = 0
        
        print(f"Starting Episode {ep + 1}")
        
        step_count = 0
        while not (done or truncated) and step_count < args.steps:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            score += reward
            step_count += 1
            
            if args.gif_name:
                frames.append(env.render())
            else:
                env.render()

        print(f"Episode {ep + 1} finished with score: {score:.2f}")

    if args.gif_name:
        print(f"Saving GIF to media/{args.gif_name}...")
        imageio.mimsave(f"media/{args.gif_name}", frames, fps=60)

    env.close()

if __name__ == "__main__":
    evaluate()
