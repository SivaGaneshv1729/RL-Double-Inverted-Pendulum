# Technical Report: Deep Reinforcement Learning for Double Inverted Pendulum Control

## Executive Summary
This report details the implementation and optimization of a Reinforcement Learning (RL) agent tasked with balancing a chaotic, double-linked inverted pendulum. Through six iterations of reward engineering and physics refinement, we successfully trained a PPO agent to achieve stable, high-precision control in a high-authority environment.

## 1. Problem Formulation: The Chaotic Pendulum
The double inverted pendulum is a classic problem in non-linear control theory. Unlike a single pendulum, the second link introduces chaotic dynamics where small changes in initial state or control force lead to divergent trajectories.
- **Degrees of Freedom**: 3 (Cart Position, Pole 1 Angle, Pole 2 Angle).
- **Control Input**: 1 (Horizontal force on the cart).
- **Underactuation**: The system is underactuated, meaning we control the poles indirectly through the cart's acceleration.

## 2. The Godzone Protocol (Iteration 6)
The primary challenge was overcoming the "Passive Survival" plateau, where the agent learned to wiggle the poles to delay falling rather than balancing perfectly. To solve this, we implemented the **Godzone Protocol**.

### 2.1 Reward Engineering
We transitioned from a continuous cosine reward to a discrete "stacked" reward system:
- **Godzone (+100.0)**: Trigged only when both poles are within $0.03 \text{ rad} (\approx 1.7^\circ)$. This creates an extremely high-gradient target.
- **Precision Zone (+20.0)**: Trigged within $0.08 \text{ rad}$.
- **Differential Penalty**: We penalized the difference between the velocity of Link 1 and Link 2 to dampen the internal "whip" effect of the chaotic system.

### 2.2 Physics Resolution
Initial failures were traced to simulation jitter. We increased the `Pymunk` sub-stepping to **40 steps per frame**. This provided the PPO agent with more consistent state transitions, reducing the noise in the reward signal.

## 3. Results Analysis
The agent was trained for **1,000,000 timesteps** using the Proximal Policy Optimization (PPO) algorithm.

### 3.1 Quantitative Metrics
| Metric | Baseline | Godzone (Final) | Improvement |
| :--- | :--- | :--- | :--- |
| **Max Steps** | 150 | **1000+** | 6.6x |
| **Average Reward** | ~250 | **~7,500** | 30x |
| **Recovery Authority** | 400 N | **800 N** | 2x |

### 3.2 Qualitative Observations
The final agent demonstrates a "high-tension" balancing style. Instead of reacting to falls, it uses the 800N authority to proactively "catch" the poles before they leave the 0.08 rad Precision Zone.

## 4. Conclusion
The "Godzone Protocol" demonstrates that in highly non-linear control tasks, **Reward Sparsity (Precision Targeting)** combined with **High-Resolution Physics** is superior to broad, continuous reward signals. The agent successfully mastered the chaotic interplay between link torques to maintain a perfect vertical stack.
