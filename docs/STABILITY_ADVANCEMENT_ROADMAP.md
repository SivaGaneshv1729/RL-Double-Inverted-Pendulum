# Stability Advancement Roadmap: Beyond the Slider

The "Clean Slate" model we just finished is physically correct and achieves stable balance, but the double pendulum is a chaotic system that can always be pushed further. Here are the four primary layers of improvement to reach "Infinite Stability."

## 1. Algorithmic Upgrades: SAC over PPO
While **PPO** (our current algorithm) is reliable, it is an "on-policy" algorithm, meaning it throws away data after every update.
- **Proposal**: Switch to **SAC (Soft Actor-Critic)**. 
- **Benefit**: SAC is "off-policy" and optimizes for **Maximum Entropy**. It explores the physics space much more thoroughly and usually finds a "tighter" balance with less jitter than PPO.

## 2. Temporal Awareness: Recurrent Policies (LSTM)
Currently, our agent has no "memory." It only sees the position *right now*. In a chaotic system, knowing where the pole was 5 milliseconds ago is vital for predicting its snap-back acceleration.
- **Proposal**: Implement an **LSTM (Long Short-Term Memory)** layer in the policy network.
- **Benefit**: This allows the agent to internalize the "momentum trends" of the pendulum, effectively giving it a sense of acceleration that raw sensors might miss due to noise.

## 3. Training Strategy: Curriculum Learning
Training the agent to balance from a random flailing start is like trying to learn to play piano by hitting random keys.
- **Proposal**: **Curriculum Learning.**
  - **Stage 1**: Train the agent to balance a single pole first.
  - **Stage 2**: "Unlock" the second pole but limit its movement range.
  - **Stage 3**: Full double-pendulum freedom.
- **Benefit**: This prevents the agent from falling into "Passive Wiggling" traps and guarantees it masters the fundamentals before moving to chaotic dynamics.

## 4. Physics Refinements: Action Smoothing & Regularization
High-authority force (800N) is powerful, but if applied too rapidly, it creates "High-Frequency Shivering" in the joints.
- **Proposal**: **Action Rate Limiting.**
  - Add a penalty to the reward function for $|\Delta u|$ (the change in force between steps).
  - Use a low-pass filter on the agent's output.
- **Benefit**: This forces the agent to use "Smooth Torque" instead of "Rapid Shoves," resulting in the fluid, fluid-like balancing seen in professional laboratory pendulums.

## 5. Domain Randomization
If the mass of a pole changes by 1 gram, a perfectly tuned agent might fail.
- **Proposal**: Randomize `pole_mass` and `pole_length` by +/- 5% at every episode terminal.
- **Benefit**: This produces a **Robust Policy** that can handle real-world manufacturing tolerances and air resistance.

---

### Suggested Implementation Order:
1. **Action Smoothing** (Easiest - 10-minute code change).
2. **SAC Algorithm** (Moderate - requires hyperparameter retuning).
3. **Curriculum Learning** (Requires multiple training scripts).
