from random import randint

import numpy as np
import pygame
import gymnasium as gym


class SnakeEnv(gym.Env):
    def __init__(self, rows=15, cols=15, render_mode="rgb_array"):
        super(SnakeEnv, self).__init__()
        self.steps = 0
        self.rows = rows
        self.cols = cols
        self.direction = 1
        # self.world = np.zeros((rows, cols))
        self.body = []
        self.head = (8, 8)
        self.food = []

        if render_mode == 'human':
            pygame.init()
            self.screen = pygame.display.set_mode((750, 750))
            pygame.display.set_caption("Maze Gym Environment")
            self.clock = pygame.time.Clock()

        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=0, high=3, shape=(15, 15), dtype=np.uint8)

    def reset(self, seed=None, options=None):
        self.steps = 0
        # self.world = np.zeros_like(self.world)
        self.body = [(8, 6), (8, 7)]
        self.head = (8, 8)
        self.food = []
        observation = self.observe()
        return observation, {}

    def step(self, action):
        reward = 0

        # if self.steps % 20 == 0:
        if len(self.food) == 0:
            self.food.append((randint(0, self.rows - 1), randint(0, self.cols - 1)))

        self.body.append(self.head)

        if action == 0:
            self.head = (self.head[0] - 1, self.head[1])
        if action == 1:
            self.head = (self.head[0] + 1, self.head[1])
        if action == 2:
            self.head = (self.head[0], self.head[1] - 1)
        if action == 3:
            self.head = (self.head[0], self.head[1] + 1)

        collision = (self.head[0] < 0 or self.head[0] >= self.rows - 1 or
                     self.head[1] < 0 or self.head[1] >= self.cols - 1 or
                     self.head in self.body)

        # self.head = self.head[0] % self.rows, self.head[1] % self.cols

        if collision:
            return None, 0, True, False, {}

        if self.head in self.food:
            self.food.remove(self.head)
            reward += 1
        else:
            # reward += 1
            del self.body[0]

        obs = self.observe()
        terminated = False
        truncated = False
        self.steps += 1
        return obs, reward, terminated, truncated, {}

    def observe(self):

        obs_size = 15
        half_size = obs_size // 2
        obs = np.zeros((obs_size, obs_size))

        head_x, head_y = self.head

        for i in range(obs_size):
            for j in range(obs_size):
                grid_x = head_x - half_size + i
                grid_y = head_y - half_size + j

                if 0 <= grid_x < self.rows and 0 <= grid_y < self.cols:
                    if (grid_x, grid_y) == self.head:
                        obs[i, j] = 2
                    elif (grid_x, grid_y) in self.body:
                        obs[i, j] = 1
                    elif (grid_x, grid_y) in self.food:
                        obs[i, j] = 3

        return obs

    def render(self, mode='rgb_array'):
        if mode == 'human':
            obs = np.zeros((self.rows, self.cols))

            for segment in self.body:
                obs[segment] = 1
            obs[self.head] = 2

            for item in self.food:
                obs[item] = 3

            # # return obs
            # obs = self.observe()
            # print(obs)
            self.screen.fill((0, 0, 0))

            for r, row in enumerate(obs):
                for c, cell in enumerate(row):
                    if cell == 1:
                        pygame.draw.rect(self.screen, (255, 100, 0), (c * 50, r * 50, 50, 50))
                    elif cell == 2:
                        pygame.draw.rect(self.screen, (255, 0, 0), (c * 50, r * 50, 50, 50))
                    elif cell == 3:
                        pygame.draw.rect(self.screen, (0, 255, 0), (c * 50, r * 50, 50, 50))

            pygame.display.flip()
            self.clock.tick(10)

        elif mode == 'rgb_array':
            return
