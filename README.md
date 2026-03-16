# Double Inverted Pendulum RL: The Godzone Protocol

A high-fidelity 2D physics-based control environment built with `Pymunk` and `Pygame`, solved using a highly-tuned Proximal Policy Optimization (PPO) agent. This project demonstrates stable control of a chaotic double inverted pendulum system through iterative reward engineering and physics sub-stepping.

## 🚀 Final Project Stats (Iteration 6)
- **Training Duration**: 1,000,000 timesteps.
- **Mean Reward**: **~7,500** (a 30x improvement over baseline).
- **Control Quality**: High-precision vertical balance within 0.03 radians.
- **Physics Fidelity**: 40 sub-steps per frame for maximum stability.

---

## 📖 Documentation
All technical details and visual walkthroughs are located in the `docs/` folder:
- **[TECHNICAL_REPORT.md](docs/TECHNICAL_REPORT.md)**: Deep dive into the control theory and "Godzone" reward engineering.
- **[WALKTHROUGH.md](docs/WALKTHROUGH.md)**: Visual guide with performance comparison and GIFs.

---

## 🛠️ Instructions to Run

### 1. Training the Agent
To train the agent with the optimized "Godzone" reward structure:
```bash
# Docker (Recommended)
docker-compose run train

# Local
python train.py --timesteps 1000000 --reward_type shaped
```

### 2. Evaluation & Visualization
To see the trained agent in action:
```bash
# To generate a performance GIF (saved to media/agent_final.gif)
docker-compose run evaluate-gif

# Local (requires a display)
python evaluate.py --model_path models/ppo_double_pendulum_shaped.zip
```

### 3. Monitoring Progress
You can track the rewards and episode lengths in real-time or via the logs:
```bash
# View the last 20 episodes
tail -n 20 logs/shaped/monitor.csv
```

---

## 🔄 How to "Reboot" (Reset) the Project
If you wish to clear all progress and start fresh (re-train from scratch):

1. **Clean the Environment**:
   ```bash
   # Removes models, logs, and compiled caches
   rm -rf models/*.zip logs/shaped/* __pycache__
   ```
2. **Reset the Media**:
   ```bash
   # Removes generated GIFs and plots
   rm -rf media/*.gif reward_comparison.png
   ```
3. **Re-run Training**:
   Follow the **Training** instructions above to restart the 1,000,000 step cycle.

---

## ⚙️ Environment Setup
- **Observation Space**: 6D vector `[cart_x, cart_vx, pole1_angle, pole1_angular_vel, pole2_angle, pole2_angular_vel]`.
- **Action Space**: 1D continuous motor force `[-1, 1]`.
- **Infrastructure**: Fully containerized via `Dockerfile` and `docker-compose.yml`.
