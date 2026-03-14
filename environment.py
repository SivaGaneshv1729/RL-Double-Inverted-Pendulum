import gymnasium as gym
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
from gymnasium import spaces
import math

class DoublePendulumEnv(gym.Env):
    """
    Custom Environment for a Double Inverted Pendulum using Pymunk for physics
    and Pygame for visualization.
    """
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, reward_type='shaped', render_mode=None):
        super(DoublePendulumEnv, self).__init__()

        self.reward_type = reward_type
        self.render_mode = render_mode

        # Physics constants
        self.dt = 1.0 / 60.0
        self.screen_width = 800
        self.screen_height = 600
        
        # Space constants
        self.cart_mass = 1.0
        self.pole1_mass = 0.5
        self.pole2_mass = 0.5
        self.pole1_length = 100.0
        self.pole2_length = 100.0
        self.force_mag = 800.0 # High authority for Iteration 6

        # Observation space: 
        # [cart_x, cart_vx, pole1_angle, pole1_angular_vel, pole2_angle, pole2_angular_vel]
        # Normalized observation space
        low = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0], dtype=np.float32)
        high = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        # Action space: Continuous force applied to the cart [-1, 1]
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

        # Pygame setup
        self.screen = None
        self.clock = None
        self.draw_options = None

        # Pymunk Space
        self.space = None
        self.cart_body = None
        self.pole1_body = None
        self.pole2_body = None

    def _setup_physics(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 981) 

        # Ground/Track
        static_body = self.space.static_body
        ground_line = pymunk.Segment(static_body, (0, self.screen_height // 2), (self.screen_width, self.screen_height // 2), 2)
        ground_line.friction = 0.5
        self.space.add(ground_line)

        # Cart
        self.cart_body = pymunk.Body(self.cart_mass, pymunk.moment_for_box(self.cart_mass, (50, 30)))
        self.cart_body.position = (self.screen_width // 2, self.screen_height // 2)
        cart_shape = pymunk.Poly.create_box(self.cart_body, (50, 30))
        cart_shape.friction = 0.5
        
        # Constraint to track
        track_joint = pymunk.GrooveJoint(static_body, self.cart_body, (0, self.screen_height // 2), (self.screen_width, self.screen_height // 2), (0, 0))
        
        # Pole 1
        moment1 = pymunk.moment_for_segment(self.pole1_mass, (0, 0), (0, -self.pole1_length), 5)
        self.pole1_body = pymunk.Body(self.pole1_mass, moment1)
        self.pole1_body.position = (self.screen_width // 2, self.screen_height // 2 - 15)
        self.pole1_body.angle = np.random.uniform(-0.01, 0.01) # Slightly increased noise for robustness
        pole1_shape = pymunk.Segment(self.pole1_body, (0, 0), (0, -self.pole1_length), 5)
        
        # Joint 1: Cart to Pole 1
        joint1 = pymunk.PivotJoint(self.cart_body, self.pole1_body, (0, -15), (0, 0))

        # Pole 2
        moment2 = pymunk.moment_for_segment(self.pole2_mass, (0, 0), (0, -self.pole2_length), 5)
        self.pole2_body = pymunk.Body(self.pole2_mass, moment2)
        self.pole2_body.position = (self.screen_width // 2, self.screen_height // 2 - 15 - self.pole1_length)
        self.pole2_body.angle = self.pole1_body.angle + np.random.uniform(-0.01, 0.01)
        pole2_shape = pymunk.Segment(self.pole2_body, (0, 0), (0, -self.pole2_length), 5)

        # Joint 2: Pole 1 to Pole 2
        joint2 = pymunk.PivotJoint(self.pole1_body, self.pole2_body, (0, -self.pole1_length), (0, 0))

        # Collision filtering (ignore collisions between connected parts)
        for shape in [cart_shape, pole1_shape, pole2_shape]:
            shape.filter = pymunk.ShapeFilter(group=1)

        self.space.add(self.cart_body, cart_shape, track_joint,
                       self.pole1_body, pole1_shape, joint1,
                       self.pole2_body, pole2_shape, joint2)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._setup_physics()
        
        # Moderate initial velocity for robustness
        self.cart_body.velocity = (np.random.uniform(-5, 5), 0)
        self.pole1_body.angular_velocity = np.random.uniform(-0.01, 0.01)
        self.pole2_body.angular_velocity = np.random.uniform(-0.01, 0.01)

        return self._get_obs(), {}

    def _get_obs(self):
        # Normalize positions relative to center and screen bounds
        cart_x = (self.cart_body.position.x - self.screen_width / 2) / (self.screen_width / 2)
        cart_vx = np.clip(self.cart_body.velocity.x / 500.0, -1.0, 1.0)
        
        def normalize_angle(a):
            return (a + np.pi) % (2 * np.pi) - np.pi

        # Angle normalized to [-1, 1] for the [-pi/2, pi/2] range 
        p1_angle = np.clip(normalize_angle(self.pole1_body.angle) / (np.pi / 2), -1.0, 1.0)
        p1_avel = np.clip(self.pole1_body.angular_velocity / 10.0, -1.0, 1.0)
        p2_angle = np.clip(normalize_angle(self.pole2_body.angle) / (np.pi / 2), -1.0, 1.0)
        p2_avel = np.clip(self.pole2_body.angular_velocity / 10.0, -1.0, 1.0)

        return np.array([cart_x, cart_vx, p1_angle, p1_avel, p2_angle, p2_avel], dtype=np.float32)

    def step(self, action):
        # Apply force
        force = action[0] * self.force_mag
        self.cart_body.apply_force_at_local_point((force, 0), (0, 0))

        # Precision physics step
        steps = 40
        for _ in range(steps):
            self.space.step(self.dt / steps)

        obs = self._get_obs()
        reward = self._calculate_reward(obs, action)
        
        # Wider limit for recovery authority verification
        cart_x, _, p1_norm_angle, _, p2_norm_angle, _ = obs
        
        limit = 0.6 # ~54 degrees
        terminated = bool(
            abs(p1_norm_angle) > limit or
            abs(p2_norm_angle) > limit or
            abs(cart_x) > 0.95
        )
        truncated = False

        if self.render_mode == "human":
            self.render()

        return obs, reward, terminated, truncated, {}

    def _calculate_reward(self, obs, action):
        cart_x, cart_vx, p1_angle, p1_avel, p2_angle, p2_avel = obs
        
        # Iteration 6: Focus on extreme precision rewards
        dist_reward = 2.0 - (p1_angle**2 + p2_angle**2)

        if self.reward_type == 'shaped':
            reward = dist_reward
            # 1. "Protocol Godzone": Extreme vertical alignment priority
            if abs(p1_angle) < 0.03 and abs(p2_angle) < 0.03:
                reward += 100.0 # Extreme reward for verticality
            elif abs(p1_angle) < 0.08 and abs(p2_angle) < 0.08:
                reward += 20.0
            
            # 2. Velocity Penalty: Heavy to discourage jitter in vertical mode
            reward -= (p1_avel**2 + p2_avel**2) * 2.0
            
            # 3. Center Penalty
            reward -= (cart_x**2) * 2.0
            
            # 4. Living Bonus: High but not dominating the Godzone bonus
            reward += 10.0 
        else:
            reward = dist_reward + 1.0

        return float(reward)

    def render(self):
        if self.render_mode is None:
            return

        if self.screen is None:
            pygame.init()
            if self.render_mode == "human":
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                pygame.display.set_caption("Double Inverted Pendulum RL")
            else: # rgb_array
                self.screen = pygame.Surface((self.screen_width, self.screen_height))
            self.clock = pygame.time.Clock()
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        self.screen.fill((255, 255, 255))
        self.space.debug_draw(self.draw_options)
        
        if self.render_mode == "human":
            pygame.display.flip()
            self.clock.tick(self.metadata["render_fps"])
        else:
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None
