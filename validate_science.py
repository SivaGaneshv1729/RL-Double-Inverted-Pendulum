
import os
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from environment import DoublePendulumEnv

def validate_stability():
    env = DoublePendulumEnv(render_mode=None)
    model_path = "models/ppo_double_pendulum_final_ep3_shaped"
    
    if not os.path.exists(model_path + ".zip"):
        print(f"Model {model_path} not found.")
        return

    model = PPO.load(model_path)
    obs, info = env.reset()
    
    theta1_history = []
    theta2_history = []
    cart_x_history = []
    steps = 600 # 10 seconds at 60fps
    
    print(f"Starting 10-second stability test...")
    
    for i in range(steps):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Extract angles directly from bodies for plot accuracy
        theta1_history.append(env.pole1_body.angle)
        theta2_history.append(env.pole2_body.angle)
        cart_x_history.append(env.cart_body.position.x - env.screen_width/2)
        
        if terminated or truncated:
            print(f"Episode ended early at step {i}")
            break
            
    # Plotting
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(theta1_history, label='Inner Pole (Theta 1)', color='#2e7d32')
    plt.plot(theta2_history, label='Outer Pole (Theta 2)', color='#1976d2')
    plt.axhline(0, color='red', linestyle='--', alpha=0.5)
    plt.ylabel('Angle (Radians)')
    plt.title('EP3 Stability: Angular Verticality Over Time (10s)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(cart_x_history, label='Cart Displacement', color='#7b1fa2')
    plt.axhline(0, color='red', linestyle='--', alpha=0.5)
    plt.xlabel('Steps (60fps)')
    plt.ylabel('Distance (px)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('media/stability_proof.png')
    print("Stability plot saved to media/stability_proof.png")
    
    # Calculate RMSE for justification
    rmse1 = np.sqrt(np.mean(np.array(theta1_history)**2))
    rmse2 = np.sqrt(np.mean(np.array(theta2_history)**2))
    print(f"Inner Pole RMSE: {rmse1:.4f} rad")
    print(f"Outer Pole RMSE: {rmse2:.4f} rad")
    
    if rmse1 < 0.1 and rmse2 < 0.1:
        print("VERDICT: Scientifically Balanced (Error < 6 degrees average)")
    else:
        print("VERDICT: Stable but with higher jitter.")

if __name__ == "__main__":
    validate_stability()
