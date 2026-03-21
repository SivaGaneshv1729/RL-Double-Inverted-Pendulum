"""
Scientific Comparison: Initial vs Final Trained Agent
Generates a 6-panel proof chart measuring RMSE, rewards, and survival.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from environment import DoublePendulumEnv
import os

def evaluate_model(model_path, label, num_episodes=3, max_steps=300):
    env = DoublePendulumEnv(render_mode=None)
    try:
        model = PPO.load(model_path)
    except Exception as e:
        print(f"  ERROR loading {model_path}: {e}")
        env.close()
        return None

    episode_rewards = []
    episode_lengths = []
    all_theta1 = []
    all_theta2 = []
    # Store first episode trace for plotting
    trace_theta1 = []
    trace_theta2 = []

    for ep in range(num_episodes):
        obs, _ = env.reset()
        ep_reward = 0
        ep_theta1 = []
        ep_theta2 = []
        for step in range(max_steps):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            theta1 = float(env.pole1_body.angle)
            theta2 = float(env.pole2_body.angle)
            ep_theta1.append(theta1)
            ep_theta2.append(theta2)
            ep_reward += reward
            if terminated or truncated:
                break
        episode_rewards.append(ep_reward)
        episode_lengths.append(len(ep_theta1))
        all_theta1.extend(ep_theta1)
        all_theta2.extend(ep_theta2)
        if ep == 0:
            trace_theta1 = ep_theta1[:]
            trace_theta2 = ep_theta2[:]
        print(f"  [{label}] Episode {ep+1}: {len(ep_theta1)} steps, reward={ep_reward:.2f}")

    env.close()

    all_t1 = np.array(all_theta1)
    all_t2 = np.array(all_theta2)
    return {
        "label": label,
        "episode_rewards": np.array(episode_rewards),
        "episode_lengths": np.array(episode_lengths),
        "rmse_theta1": float(np.sqrt(np.mean(all_t1**2))),
        "rmse_theta2": float(np.sqrt(np.mean(all_t2**2))),
        "trace_theta1": np.degrees(trace_theta1),
        "trace_theta2": np.degrees(trace_theta2),
    }

def main():
    print("=" * 55)
    print("  SCIENTIFIC MODEL COMPARISON")
    print("=" * 55)

    initial_path = "models/ppo_baseline_baseline"
    final_path   = "models/ppo_shaped_500k_shaped"

    print(f"\nEvaluating Initial model ({initial_path})...")
    initial = evaluate_model(initial_path, "Initial (5k steps)")

    print(f"\nEvaluating Final model ({final_path})...")
    final = evaluate_model(final_path, "Final (500k steps)")

    if initial is None or final is None:
        print("Cannot compare — check model paths.")
        return

    # --- Print Results Table ---
    print("\n" + "=" * 55)
    print(f"  {'Metric':<30} {'Initial':>10} {'Final':>10}")
    print("  " + "-" * 51)
    def row(name, iv, fv, fmt=".2f"):
        print(f"  {name:<30} {iv:>{10}.{fmt[1:]}} {fv:>{10}.{fmt[1:]}}")

    r_i_mean = initial['episode_rewards'].mean()
    r_f_mean = final['episode_rewards'].mean()
    l_i_mean = initial['episode_lengths'].mean()
    l_f_mean = final['episode_lengths'].mean()
    rm1_i = np.degrees(initial['rmse_theta1'])
    rm1_f = np.degrees(final['rmse_theta1'])
    rm2_i = np.degrees(initial['rmse_theta2'])
    rm2_f = np.degrees(final['rmse_theta2'])

    print(f"  {'Mean Survival Steps':<30} {l_i_mean:>10.1f} {l_f_mean:>10.1f}")
    print(f"  {'Mean Episode Reward':<30} {r_i_mean:>10.2f} {r_f_mean:>10.2f}")
    print(f"  {'Inner Pole RMSE (degrees)':<30} {rm1_i:>10.2f} {rm1_f:>10.2f}")
    print(f"  {'Outer Pole RMSE (degrees)':<30} {rm2_i:>10.2f} {rm2_f:>10.2f}")
    print("=" * 55)
    if r_f_mean > r_i_mean:
        print(f"  Reward improvement: {r_f_mean/max(r_i_mean,0.001):.2f}x higher")
    if rm1_f < rm1_i:
        print(f"  Inner Pole: {rm1_i:.2f}° -> {rm1_f:.2f}° RMSE ({rm1_i/max(rm1_f,0.001):.2f}x more stable)")
    if rm2_f < rm2_i:
        print(f"  Outer Pole: {rm2_i:.2f}° -> {rm2_f:.2f}° RMSE ({rm2_i/max(rm2_f,0.001):.2f}x more stable)")

    # --- Generate Chart ---
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor('#1a1a2e')
    colors = {'initial': '#e74c3c', 'final': '#2ecc71'}

    def sax(ax, title):
        ax.set_facecolor('#16213e')
        ax.set_title(title, color='white', fontsize=10, pad=6)
        ax.tick_params(colors='#aaaaaa', labelsize=8)
        ax.grid(True, alpha=0.2, color='#556677')
        for s in ax.spines.values():
            s.set_edgecolor('#445566')

    # Row 0: Inner Pole Traces
    ax = axes[0][0]
    ax.plot(np.array(initial['trace_theta1'][:500]), color=colors['initial'], lw=1)
    ax.axhline(0, color='white', ls='--', alpha=0.5, lw=1)
    ax.set_ylabel('Angle (°)', color='#aaa', fontsize=8)
    ax.set_xlabel('Steps', color='#aaa', fontsize=8)
    sax(ax, f"INITIAL — Inner Pole Angle\n(RMSE: {rm1_i:.2f}°)")

    ax = axes[0][1]
    ax.plot(np.array(final['trace_theta1'][:500]), color=colors['final'], lw=1)
    ax.axhline(0, color='white', ls='--', alpha=0.5, lw=1)
    ax.set_ylabel('Angle (°)', color='#aaa', fontsize=8)
    ax.set_xlabel('Steps', color='#aaa', fontsize=8)
    sax(ax, f"FINAL — Inner Pole Angle\n(RMSE: {rm1_f:.2f}°)")

    # RMSE Bar Chart
    ax = axes[0][2]
    cats = ['Inner Pole\nRMSE (°)', 'Outer Pole\nRMSE (°)']
    xi = np.arange(len(cats))
    ax.bar(xi - 0.2, [rm1_i, rm2_i], 0.35, color=colors['initial'], label='Initial', alpha=0.9)
    ax.bar(xi + 0.2, [rm1_f, rm2_f], 0.35, color=colors['final'],   label='Final',   alpha=0.9)
    ax.set_xticks(xi)
    ax.set_xticklabels(cats, color='#aaa', fontsize=8)
    ax.legend(fontsize=9, facecolor='#16213e', labelcolor='white')
    ax.set_ylabel('RMSE (°)', color='#aaa', fontsize=8)
    sax(ax, 'Pole RMSE: Initial vs Final\n(Lower is Better ✓)')

    # Row 1: Outer Pole Traces
    ax = axes[1][0]
    ax.plot(np.array(initial['trace_theta2'][:500]), color=colors['initial'], lw=1)
    ax.axhline(0, color='white', ls='--', alpha=0.5, lw=1)
    ax.set_ylabel('Angle (°)', color='#aaa', fontsize=8)
    ax.set_xlabel('Steps', color='#aaa', fontsize=8)
    sax(ax, f"INITIAL — Outer Pole Angle\n(RMSE: {rm2_i:.2f}°)")

    ax = axes[1][1]
    ax.plot(np.array(final['trace_theta2'][:500]), color=colors['final'], lw=1)
    ax.axhline(0, color='white', ls='--', alpha=0.5, lw=1)
    ax.set_ylabel('Angle (°)', color='#aaa', fontsize=8)
    ax.set_xlabel('Steps', color='#aaa', fontsize=8)
    sax(ax, f"FINAL — Outer Pole Angle\n(RMSE: {rm2_f:.2f}°)")

    # Per-Episode Rewards
    ax = axes[1][2]
    eps = np.arange(1, len(initial['episode_rewards']) + 1)
    ax.bar(eps - 0.2, initial['episode_rewards'], 0.35, color=colors['initial'], label='Initial', alpha=0.9)
    ax.bar(eps + 0.2, final['episode_rewards'],   0.35, color=colors['final'],   label='Final',   alpha=0.9)
    ax.legend(fontsize=9, facecolor='#16213e', labelcolor='white')
    ax.set_xlabel('Episode', color='#aaa', fontsize=8)
    ax.set_ylabel('Total Reward', color='#aaa', fontsize=8)
    sax(ax, 'Per-Episode Rewards (5 runs)\n(Higher is Better ✓)')

    fig.suptitle(
        'Proof of Stabilisation: Initial (5k steps) vs Trained (500k steps)',
        color='white', fontsize=13, fontweight='bold'
    )

    # Summary footer
    lines = [
        f"Inner Pole RMSE:  {rm1_i:.2f}° → {rm1_f:.2f}°",
        f"Outer Pole RMSE:  {rm2_i:.2f}° → {rm2_f:.2f}°",
        f"Mean Reward:  {r_i_mean:.1f} → {r_f_mean:.1f}",
    ]
    fig.text(0.5, 0.01, "   |   ".join(lines), ha='center', color='#aaffaa', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='#0f3460', alpha=0.8))

    plt.tight_layout(rect=[0, 0.04, 1, 0.95])
    out = 'media/proof_of_stabilization.png'
    plt.savefig(out, dpi=140, facecolor='#1a1a2e', bbox_inches='tight')
    print(f"\nProof chart saved to: {out}")

if __name__ == "__main__":
    main()
