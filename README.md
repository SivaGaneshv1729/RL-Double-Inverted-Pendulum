# Deep Reinforcement Learning: Double Inverted Pendulum Control

A high-fidelity 2D physics-based control environment built with `Pymunk` and `Pygame`, solved using Proximal Policy Optimization (PPO). The agent learns to balance two linked poles on a sliding cart by applying horizontal forces.

---

### Environment Design

The environment (`environment.py`) simulates a double inverted pendulum using the `Pymunk` 2D rigid-body physics engine:

- **Cart**: A box body constrained to a horizontal track via a `GrooveJoint`. Its moment of inertia is set to `float('inf')` so it can only *slide* — no rotation.
- **Poles**: Two `Segment` bodies connected with `PivotJoint` constraints — Pole 1 pivots on the cart, Pole 2 pivots on the tip of Pole 1.
- **Physics Resolution**: 40 sub-steps per frame (`dt/40`) for simulation stability.
- **Rendering**: `pygame` draws the `pymunk` space each frame. Supports `human` (window) and `rgb_array` (GIF/video) modes.

**Observation Space (6D)**:

| Index | Variable | Description |
|-------|----------|-------------|
| 0 | `cart_x` | Normalized horizontal cart position [-1, 1] |
| 1 | `cart_vx` | Normalized cart velocity |
| 2 | `theta1` | Inner pole angle (radians) |
| 3 | `omega1` | Inner pole angular velocity |
| 4 | `theta2` | Outer pole angle (radians) |
| 5 | `omega2` | Outer pole angular velocity |

**Action Space (1D)**: Continuous force value in [-1.0, 1.0], scaled by `force_mag = 800 N`.

---

### Reward Function Design

Two reward functions are implemented, selectable via `--reward_type`:

#### Baseline Reward (`reward_type='baseline'`)
$$R = \cos(\theta_1) + \cos(\theta_2)$$

The simplest possible reward. Returns maximum value of **+2** when both poles are perfectly vertical (angle = 0), and approaches **-2** when both are fully inverted (angle = π). Provides no guidance on cart position or movement quality.

#### Shaped Reward (`reward_type='shaped'`)
$$R = \underbrace{(\cos\theta_1 + \cos\theta_2)}_{\text{Upright Bonus}} - \underbrace{|x| \times 0.3}_{\text{Center Penalty}} - \underbrace{(|\dot\theta_1| + |\dot\theta_2|) \times 0.01}_{\text{Velocity Penalty}} - \underbrace{u^2 \times 0.001}_{\text{Action Penalty}}$$

| Term | Purpose |
|------|---------|
| **Upright Bonus** | Core goal: maintain both poles vertically aligned |
| **Center Penalty** | Prevents cart from drifting to track edges |
| **Velocity Penalty** | Encourages smooth, calm micro-corrections |
| **Action Penalty** | Penalizes wasteful energy usage |

The shaped reward converges significantly faster than the baseline because it provides dense, informative feedback at every timestep.

---

### How to Run

#### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed and running.

#### 1. Build the Docker Image
```bash
docker-compose build
```

#### 2. Train the Agent
```bash
# Train with shaped reward (recommended) for 200,000 timesteps
docker-compose run train

# Train with baseline reward
docker-compose run train-baseline

# Custom local training
python train.py --timesteps 500000 --reward_type shaped --save_path models/my_model
```

#### 3. Evaluate & Visualize
```bash
# Generate evaluation GIF (headless, no display required)
docker-compose run evaluate-gif

# Live window evaluation (requires display)
python evaluate.py --model_path models/ppo_double_pendulum_final_ep3_shaped
```

#### 4. View Training Logs
```bash
# Monitor live reward progress
tail -f logs/shaped/monitor.csv
```

#### 5. Generate Reward Comparison Plot
```bash
python plot_results.py --log_dir logs/shaped --output reward_comparison.png
```

---

## Project Stats
- **Observation Space**: 6D `[cart_x, vx, θ₁, ω₁, θ₂, ω₂]`
- **Action Space**: 1D continuous force `[-1.0, 1.0]`
- **Algorithm**: PPO (Proximal Policy Optimization) via `stable-baselines3`
- **Physics Engine**: `Pymunk` 2D rigid-body simulation
- **Container**: Fully Dockerized with headless rendering via `Xvfb`

---

## File Structure

```
.
├── environment.py          # Custom Gymnasium environment
├── train.py                # Training script (PPO)
├── evaluate.py             # Evaluation + GIF generation
├── plot_results.py         # Reward comparison plot
├── validate_science.py     # Quantitative stability metrics
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── models/                 # Saved model weights
├── logs/                   # Training logs (CSV)
├── media/                  # GIFs and plots
└── docs/                   # Technical documentation
```
