"""
generate_initial_gif.py
Generates agent_initial.gif using RANDOM actions (completely untrained).
This makes the visual contrast with agent_final.gif immediately obvious —
the untrained agent just falls in seconds with chaotic motion.
"""
import os
import numpy as np
import imageio
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # headless
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from environment import DoublePendulumEnv

def generate_random_gif(out_path='media/agent_initial.gif', max_steps=120, fps=30):
    env = DoublePendulumEnv(render_mode='rgb_array')
    obs, _ = env.reset()
    frames = []

    for step in range(max_steps):
        # PURELY RANDOM action — no model, no learning, just noise
        action = env.action_space.sample()
        obs, reward, terminated, truncated, _ = env.step(action)
        frame = env.render()
        if frame is not None:
            frames.append(frame.astype(np.uint8))
        if terminated or truncated:
            print(f"  Random agent fell at step {step+1}")
            # Pad with last frame to show it collapsed
            for _ in range(10):
                frames.append(frames[-1])
            break

    env.close()

    os.makedirs('media', exist_ok=True)
    imageio.mimsave(out_path, frames, fps=fps)
    print(f"Saved: {out_path} ({len(frames)} frames)")

if __name__ == '__main__':
    print("Generating RANDOM agent GIF (untrained - will fall immediately)...")
    generate_random_gif()
