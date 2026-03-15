# Double Inverted Pendulum Reinforcement Learning: The Godzone Protocol

A high-fidelity 2D physics-based control environment built with `Pymunk` and `Pygame`, solved using a highly-tuned Proximal Policy Optimization (PPO) agent. This project demonstrates stable control of a chaotic double inverted pendulum system through iterative reward engineering and physics sub-stepping.

## Environment Design
The environment simulates a cart on a 1D track with a double-linked pendulum attached, characterized by its non-linear and chaotic dynamics.
- **Physics Engine**: `Pymunk` with high-resolution sub-stepping (40 steps per frame).
- **Visualization**: `Pygame` for real-time rendering and evaluation.
- **Observation Space**: 6D vector `[cart_x, cart_vx, pole1_angle, pole1_angular_vel, pole2_angle, pole2_angular_vel]`.
- **Action Space**: 1D continuous motor force `[-1, 1]` with an 800.0 authority magnitude.

## The Godzone Protocol (Iteration 6)
The project culminated in "The Godzone Protocol," a reward structure designed to forcefully incentivize high-precision verticality over passive survival.

### Reward Function Components:
1. **Verticality Bonus (Godzone)**: **+100.0** reward for maintaining both poles within 0.03 radians of vertical.
2. **Precision Bonus**: **+20.0** reward for maintaining both poles within 0.08 radians.
3. **Living Bonus**: **+10.0** survival reward (reduced from earlier iterations to prioritize quality).
4. **Kinetic Penalty**: Heavy penalties for high angular velocity to suppress high-frequency jitter.
5. **Center Constraint**: Quadratic penalty for distance from the track center.

## Performance Justification
Through six iterations of tuning, the agent reached the following milestones:
- **Training Epochs**: 1,000,000 timesteps.
- **Reward Growth**: 30x increase from baseline (~250 to ~7,500+).
- **Stability**: Recovery authority increased to 800, enabling the agent to save trajectories from 50+ degree tilts.

## How to Run

### Setup with Docker
The project is fully containerized for reproducible results.

1. **Build the image**:
   ```bash
   docker-compose build
   ```

2. **Train the agent (Iteration 6)**:
   ```bash
   docker-compose run train
   ```

3. **Evaluate and visualize**:
   Captures the agent in action and saves a GIF to `media/agent_final.gif`:
   ```bash
   docker-compose run evaluate-gif
   ```

### Local Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Train: `python train.py --timesteps 1000000 --reward_type shaped`
3. Evaluate: `python evaluate.py --model_path models/ppo_double_pendulum_shaped.zip`

## Documentation & Analysis
- **[TECHNICAL_REPORT.md](TECHNICAL_REPORT.md)**: Deep dive into the control theory and reward engineering choices.
- **[walkthrough.md](C:\Users\user\.gemini\antigravity\brain\299460ea-1a97-4486-878c-d33c0a53ba8d\walkthrough.md)**: Visual walkthrough with demonstration GIFs.
