# 🎬 Final Presentation Script & Running Steps
## Project: Deep RL for Double Inverted Pendulum Control

---

## Part 1: Project Demo Running Steps

### Step 1 — Build Docker Image
```bash
docker-compose build
```
*"I have containerized the entire project with Docker. One command installs Python 3.9, Pymunk, Pytorch, Stable-Baselines3, and the virtual framebuffer."*

### Step 2 — Train with Both Reward Functions
```bash
# Shaped reward (recommended for best results)
docker-compose run train

# Baseline reward (for comparison)
docker-compose run train-baseline
```
*"I implemented two reward functions as required. The baseline reward is `cos(θ₁) + cos(θ₂)`, rewarding uprightness only. The shaped reward adds a center penalty, velocity penalty, and action penalty for much faster learning."*

### Step 3 — Generate the Evaluation GIF
```bash
docker-compose run evaluate-gif
```
*"This runs the trained brain headlessly via Xvfb and saves a GIF — no physical monitor needed."*

### Step 4 — View Learning Curves
```bash
python plot_results.py
```
*"This produces `reward_comparison.png`, showing both reward curves side-by-side over 200k training steps."*

---

## Part 2: Video Presentation Script

### [INTRO — Show title screen]
> "Hello. I've built a complete Reinforcement Learning system to solve one of the hardest classical control problems: balancing a double inverted pendulum. This is harder than the famous CartPole — we have two linked poles that must both stay upright simultaneously."

---

### [Screen Share — Show `environment.py`]
> "I built the physics simulation from scratch using **Pymunk**, a 2D rigid-body engine. I use:
> - A `GrooveJoint` to lock the cart to a horizontal track, so it can only **slide** — just like a real-world lab pendulum.
> - Two `PivotJoint` connections — one between cart and pole 1, and one between pole 1 and pole 2.
> - 40 physics sub-steps per render frame for simulation accuracy.
>
> The observation space is a **6D vector**: `[cart_x, vx, θ₁, ω₁, θ₂, ω₂]`, giving the agent complete knowledge of the system state."

---

### [Screen Share — Show `_calculate_reward` in `environment.py`]
> "Reward engineering is the scientific heart of this project.
>
> My **baseline reward** is simply `cos(θ₁) + cos(θ₂)`. It's maximal at +2 when both poles are upright and falls to -2 when fully inverted. This is the minimum necessary signal.
>
> My **shaped reward** builds on this with three additional terms:
> - A **center penalty** that prevents the cart from drifting to the track limits.
> - A **velocity penalty** that discourages chaotic oscillations.
> - An **action penalty** that reduces wasted energy.
>
> This 'Reward Shaping' technique is a cornerstone of practical RL and is why the shaped agent converges much faster."

---

### [Screen Share — Show `reward_comparison.png`]
> "Here is the empirical proof. Both agents were trained for 200,000 PPO timesteps. The shaped reward (top line) consistently achieves higher and more stable rewards because it provides richer feedback at every step."

---

### [Screen Share — Show `media/agent_initial.gif`]
> "This is the early-stage agent — essentially random exploration. Watch how the poles immediately fall and the cart shows no directional strategy."

### [Screen Share — Show `media/agent_final.gif`]
> "And here is the trained agent. The base is now correctly **sliding left and right** — not rotating. The agent has learned to use micro-corrections to keep both poles balanced in their equilibrium position."

---

### [Screen Share — Show Terminal `docker-compose build`]
> "The entire project is containerized with Docker. I use `Xvfb` — a virtual framebuffer — to allow headless GIF generation inside the container, even without a physical monitor. This ensures the project runs identically on any machine."

---

### [OUTRO]
> "In summary, I've built a complete RL pipeline: a physically-accurate custom gym environment, two scientifically-designed reward functions, a fully-automated training and evaluation pipeline, and a reproducible Docker infrastructure.
>
> The final trained agent balances a chaotic double inverted pendulum by sliding a cart along a track — the same principle used to control bipedal robots and precision robotic arms. Thank you."

---

## Part 3: Quick Command Reference Card

| Goal | Command |
|------|---------|
| Build Docker | `docker-compose build` |
| Train (shaped) | `docker-compose run train` |
| Train (baseline) | `docker-compose run train-baseline` |
| Generate GIF | `docker-compose run evaluate-gif` |
| Live evaluation | `python evaluate.py --model_path models/ppo_shaped_v2_shaped` |
| Plot rewards | `python plot_results.py` |
| Check logs | `tail -f logs/shaped/monitor.csv` |
