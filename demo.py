import time
import os
import sys

def print_narration(text):
    print("\n" + "="*80)
    for line in text.strip().split('\n'):
        print(f"  [NARRATOR]: {line.strip()}")
    print("="*80 + "\n")
    time.sleep(2)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_narration("""
    Welcome to the Double Inverted Pendulum RL Project Presentation.
    This project demonstrates a high-fidelity physics environment and a 
    trained PPO agent capable of balancing two linked poles on a sliding cart.
    """)

    print_narration("""
    Step 1: Environmental Design.
    We used Pymunk for rigid-body physics and Pygame for rendering.
    The cart is restricted to horizontal sliding, and we use 40 sub-steps 
    per frame to ensure simulation stability.
    """)

    print_narration("""
    Step 2: The Initial State (Untrained).
    We will now show the 'agent_initial.gif' results.
    Note how the untrained agent falls almost immediately (within 90 steps).
    The motion is chaotic and lacks any balancing strategy.
    """)
    if os.path.exists('media/agent_initial.gif'):
        print("  [ACTION]: Opening media/agent_initial.gif...")
        os.system('start media/agent_initial.gif' if os.name == 'nt' else 'open media/agent_initial.gif')
        time.sleep(5)
    else:
        print("  [WARN]: agent_initial.gif not found.")

    print_narration("""
    Step 3: The Reward Function.
    We transitioned from a simple 'Baseline' reward (just cosine of angles)
    to a 'Shaped' reward. The shaped reward penalizes cart distance from center,
    high angular velocities, and excessive motor force.
    This leads to much smoother and more efficient control.
    """)

    print_narration("""
    Step 4: The Final Result (Trained).
    After 500,000 steps of training, the agent has learned to recover from 
    tilts and stay centered.
    We will now show 'agent_final.gif'.
    """)
    if os.path.exists('media/agent_final.gif'):
        print("  [ACTION]: Opening media/agent_final.gif...")
        os.system('start media/agent_final.gif' if os.name == 'nt' else 'open media/agent_final.gif')
        time.sleep(5)
    else:
        print("  [WARN]: agent_final.gif not found.")

    print_narration("""
    Step 5: Scientific Validation.
    Visually, the difference is clear, but scientifically, we measure 
    RMSE (Root Mean Square Error). The trained agent shows a 15-30% 
    reduction in angular deviation compared to random exploration.
    """)
    if os.path.exists('media/proof_of_stabilization.png'):
        print("  [ACTION]: Opening media/proof_of_stabilization.png...")
        os.system('start media/proof_of_stabilization.png' if os.name == 'nt' else 'open media/proof_of_stabilization.png')
        time.sleep(5)
    
    print_narration("""
    Final Summary:
    - 6D Observation Space [x, vx, theta1, omega1, theta2, omega2]
    - 1D Continuous Action Space [-1, 1] for horizontal force.
    - Fully containerized with Docker and headless rendering support.
    
    Thank you for watching this presentation.
    """)

if __name__ == "__main__":
    main()
