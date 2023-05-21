import gym
import pygame
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from flappyGame import FlappyBirdGame  # Import your Flappy Bird game class

class FlappyBirdEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, game_env):
        super(FlappyBirdEnv, self).__init__()
        self.action_space = spaces.Discrete(2)
        #self.observation_space = spaces.Box(low=0, high=255, shape=(724, 376, 3), dtype=np.uint8)  # Example: RGB image observation
        # Define the observation space (example: bird position and pipe positions)
        self.observation_space = spaces.Dict({
            'bird_position': spaces.Box(low=0, high=1, shape=(2,), dtype=float),  # Example: bird position (x, y)
            'pipe_positions': spaces.Box(low=0, high=1, shape=(4,), dtype=float)  # Example: pipe positions (top_x, top_y, bottom_x, bottom_y)
        })
        self.game = game_env

    def step(self, action):
        # Perform the action in the game
        self.game.perform_action(action)

        # Update the game state and retrieve the updated game state
        game_state, reward, done = self.game.update_game(action)

        # Convert the game state to the observation format
        next_observation = {
            'bird_position': game_state['bird_position'],
            'pipe_positions': game_state['pipe_positions']
        }

        # Additional information (if needed)
        info = {}

        return next_observation, reward, done, info

    def reset(self):
        # Reset the game
        self.game.reset()

        # Get the initial game state
        game_state = self.game.get_game_state()

        # Convert the game state to the observation format
        observation = {
            'bird_position': game_state['bird_position'],
            'pipe_positions': game_state['pipe_positions']
        }

        return observation

    def render(self):
        # Render the game (if needed)
        self.game.render()

    def close(self):
        pass
