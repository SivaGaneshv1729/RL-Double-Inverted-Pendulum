# Double Inverted Pendulum Reinforcement Learning

A custom 2D physics-based control environment built with `Pymunk` and `Pygame`, solved using the Proximal Policy Optimization (PPO) algorithm.

## Environment Design
The environment simulates a cart on a 1D track with a double-linked pendulum attached.
- **Physics Engine**: `Pymunk` handles gravity, constraints, and forces.
- **Visualization**: `Pygame` renders the simulation.
- **Observation Space**: A 6D vector containing `[cart_x, cart_vx, pole1_angle, pole1_angular_vel, pole2_angle, pole2_angular_vel]`.
- **Action Space**: A 1D continuous value `[-1, 1]` representing the horizontal force applied to the cart.

## Reward Function Design

### Baseline Reward
The baseline reward is a simple function of the verticality of both poles:
$$R = \cos(\theta_1) + \cos(\theta_2)$$
This provides a gradient that is maximal when both poles are perfectly upright and zero when they are horizontal.

### Shaped Reward
The shaped reward introduces additional terms to guide the agent's behavior and speed up learning:
1. **Upright Bonus**: The baseline $\cos(\theta_1) + \cos(\theta_2)$ term.
2. **Center Penalty**: $-|x| \times 0.1$, which discourages the agent from moving too far from the center or running off-screen.
3. **Velocity Penalty**: $- (|\omega_1| + |\omega_2|) \times 0.01$, which penalizes high angular velocities to encourage stable, smooth movements.
4. **Action Penalty**: $- a^2 \times 0.001$, which penalizes excessive force usage.
5. **Survival Bonus**: $+0.1$ for every step the episode survives without the poles falling over or the cart going off-screen.

## How to Run

### Setup with Docker
The project is fully containerized. Ensure you have Docker and Docker Compose installed.

1. **Build the image**:
   ```bash
   docker-compose build
   ```

2. **Train the agent (Shaped Reward)**:
   ```bash
   docker-compose run train
   ```

3. **Train the agent (Baseline Reward)**:
   ```bash
   docker-compose run train-baseline
   ```

4. **Evaluate and visualize**:
   To see the agent in action (requires X11 forwarding on Linux/Mac or XServer on Windows like VcXsrv):
   ```bash
   docker-compose run evaluate
   ```

5. **Generate a GIF for evaluation**:
   This runs headlessly inside the container and saves a GIF to `media/agent_final.gif`:
   ```bash
   docker-compose run evaluate-gif
   ```

### Local Setup (Alternative)
If you prefer running locally:
1. Install dependencies: `pip install -r requirements.txt`
2. Train: `python train.py --timesteps 200000 --reward_type shaped`
3. Plot results: `python plot_results.py`
4. Evaluate: `python evaluate.py --model_path models/ppo_double_pendulum_shaped.zip`

## Results
The performance comparison between the baseline and shaped rewards can be found in `reward_comparison.png`. Demo GIFs are located in the `media/` directory.
